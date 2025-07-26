"""
Whisper service for audio transcription of Quran recitations
Updated for OpenAI Python client v1.56+ with async support
"""

import os
from openai import AsyncOpenAI
from typing import Dict, Any, BinaryIO
import tempfile
import logging
import asyncio
import aiofiles

from .ai_service import AIService, AIServiceError, AIAnalysisResult

logger = logging.getLogger(__name__)

class WhisperService(AIService):
    """OpenAI Whisper service for audio transcription with async support"""
    
    def __init__(self):
        super().__init__()
        self.api_key = self.validate_api_key(os.getenv("OPENAI_API_KEY"))
        # Use AsyncOpenAI for better performance with FastAPI
        self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Enhanced model and format support
        self.model = "whisper-1"  # Latest Whisper model
        self.supported_formats = {
            'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm', 'ogg', 'flac'
        }
        self.max_file_size = 25 * 1024 * 1024  # 25MB OpenAI limit
    
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process audio data with Whisper"""
        try:
            if isinstance(input_data, dict) and "audio_file" in input_data:
                return await self.transcribe_audio(
                    input_data["audio_file"],
                    language=input_data.get("language", "ar"),
                    prompt=input_data.get("prompt")
                )
            else:
                raise AIServiceError("Invalid input data format for Whisper")
        except Exception as e:
            await self.handle_api_error(e, "Whisper processing")
    
    async def transcribe_audio(
        self, 
        audio_file: BinaryIO, 
        language: str = "ar",
        prompt: str = None
    ) -> AIAnalysisResult:
        """Transcribe audio file using Whisper with async support"""
        try:
            # Validate file first
            self.validate_audio_file(audio_file)
            
            # Enhanced prompt for better Arabic/Quranic transcription
            if not prompt:
                prompt = "بسم الله الرحمن الرحيم، القرآن الكريم، السورة، الآية، التلاوة، التجويد"
            
            # Create a temporary file asynchronously
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # Write audio data to temporary file
                audio_content = audio_file.read()
                temp_file.write(audio_content)
                temp_file.flush()
                
                try:
                    # Transcribe using async Whisper client
                    with open(temp_file.name, "rb") as audio:
                        transcript = await self.client.audio.transcriptions.create(
                            model=self.model,
                            file=audio,
                            language=language,
                            prompt=prompt,
                            response_format="verbose_json",
                            temperature=0.0  # More deterministic for religious content
                        )
                    
                    return AIAnalysisResult(
                        success=True,
                        data={
                            "text": transcript.text,
                            "language": transcript.language,
                            "duration": transcript.duration,
                            "segments": getattr(transcript, 'segments', [])
                        },
                        confidence=self._calculate_confidence(transcript),
                        metadata={
                            "model": self.model,
                            "type": "audio_transcription",
                            "language": language,
                            "api_version": "v1.56+"
                        }
                    )
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
                
        except Exception as e:
            return AIAnalysisResult(
                success=False,
                error=f"Audio transcription failed: {str(e)}"
            )
    
    async def transcribe_with_timestamps(
        self, 
        audio_file: BinaryIO, 
        language: str = "ar"
    ) -> AIAnalysisResult:
        """Transcribe audio with detailed timestamps using async client"""
        try:
            # Validate file first
            self.validate_audio_file(audio_file)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                audio_content = audio_file.read()
                temp_file.write(audio_content)
                temp_file.flush()
                
                try:
                    with open(temp_file.name, "rb") as audio:
                        transcript = await self.client.audio.transcriptions.create(
                            model=self.model,
                            file=audio,
                            language=language,
                            response_format="verbose_json",
                            timestamp_granularities=["word", "segment"],
                            temperature=0.0
                        )
                    
                    return AIAnalysisResult(
                        success=True,
                        data={
                            "text": transcript.text,
                            "language": transcript.language,
                            "duration": transcript.duration,
                            "words": getattr(transcript, 'words', []),
                            "segments": getattr(transcript, 'segments', [])
                        },
                        confidence=self._calculate_confidence(transcript),
                        metadata={
                            "model": self.model,
                            "type": "timestamped_transcription",
                            "language": language,
                            "api_version": "v1.56+"
                        }
                    )
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
                
        except Exception as e:
            return AIAnalysisResult(
                success=False,
                error=f"Timestamped transcription failed: {str(e)}"
            )
    
    def _calculate_confidence(self, transcript) -> float:
        """Calculate confidence score from transcript data"""
        try:
            # If segments are available, calculate average confidence
            if hasattr(transcript, 'segments') and transcript.segments:
                confidences = []
                for segment in transcript.segments:
                    if hasattr(segment, 'avg_logprob'):
                        # Convert log probability to confidence (rough estimation)
                        confidence = min(1.0, max(0.0, (segment.avg_logprob + 1.0)))
                        confidences.append(confidence)
                
                if confidences:
                    return sum(confidences) / len(confidences)
            
            # Fallback: estimate based on transcript length and quality
            text_length = len(transcript.text.strip())
            if text_length > 50:
                return 0.85  # High confidence for longer transcripts
            elif text_length > 10:
                return 0.70  # Medium confidence
            else:
                return 0.50  # Low confidence for very short transcripts
                
        except Exception:
            return 0.75  # Default confidence
    
    async def detect_language(self, audio_file: BinaryIO) -> AIAnalysisResult:
        """Detect the language of the audio file using async client"""
        try:
            # Validate file first
            self.validate_audio_file(audio_file)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                audio_content = audio_file.read()
                temp_file.write(audio_content)
                temp_file.flush()
                
                try:
                    with open(temp_file.name, "rb") as audio:
                        # Use transcription with language detection
                        result = await self.client.audio.transcriptions.create(
                            model=self.model,
                            file=audio,
                            response_format="verbose_json",
                            temperature=0.0
                        )
                    
                    return AIAnalysisResult(
                        success=True,
                        data={
                            "detected_language": result.language,
                            "text_sample": result.text[:100] + "..." if len(result.text) > 100 else result.text,
                            "confidence_score": self._calculate_confidence(result)
                        },
                        confidence=0.8,
                        metadata={
                            "model": self.model,
                            "type": "language_detection",
                            "api_version": "v1.56+"
                        }
                    )
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
                
        except Exception as e:
            return AIAnalysisResult(
                success=False,
                error=f"Language detection failed: {str(e)}"
            )
    
    def validate_audio_file(self, audio_file: BinaryIO) -> bool:
        """Validate audio file format and size"""
        try:
            # Check file size (OpenAI Whisper has 25MB limit)
            audio_file.seek(0, 2)  # Seek to end
            file_size = audio_file.tell()
            audio_file.seek(0)  # Reset to beginning
            
            if file_size > self.max_file_size:
                raise AIServiceError(
                    f"Audio file too large: {file_size} bytes (max: {self.max_file_size} bytes)"
                )
            
            if file_size == 0:
                raise AIServiceError("Audio file is empty")
            
            # Check if we can get file name for format validation
            if hasattr(audio_file, 'name') and audio_file.name:
                file_extension = audio_file.name.split('.')[-1].lower()
                if file_extension not in self.supported_formats:
                    raise AIServiceError(
                        f"Unsupported audio format: {file_extension}. "
                        f"Supported formats: {', '.join(self.supported_formats)}"
                    )
            
            return True
            
        except Exception as e:
            if isinstance(e, AIServiceError):
                raise
            raise AIServiceError(f"Audio file validation failed: {str(e)}") 