"""
Gemini AI service for text analysis and coaching insights
"""

import os
from google import genai  # New Google GenAI SDK (2025)
from typing import Dict, Any, List
import json
import logging
import asyncio

from .ai_service import AIService, AIServiceError, AIAnalysisResult

logger = logging.getLogger(__name__)

class GeminiService(AIService):
    """Gemini AI service using the new Google GenAI SDK (2025)"""
    
    def __init__(self):
        super().__init__()
        self.api_key = self.validate_api_key(os.getenv("GEMINI_API_KEY"))
        
        # Initialize the new Google GenAI client
        self.client = genai.Client(api_key=self.api_key)
        
        # Use latest Gemini 2.0 Flash model
        self.model_name = 'gemini-2.0-flash-exp'
        
        # Enhanced safety settings for Islamic content
        self.safety_settings = [
            genai.types.SafetySetting(
                category=genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            ),
            genai.types.SafetySetting(
                category=genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            ),
            genai.types.SafetySetting(
                category=genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            ),
            genai.types.SafetySetting(
                category=genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            )
        ]
    
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input data with Gemini AI"""
        try:
            if isinstance(input_data, str):
                response = await self.generate_text(input_data)
            elif isinstance(input_data, dict):
                if "analyze_mistakes" in input_data:
                    response = await self.analyze_mistakes(input_data["mistakes"])
                elif "generate_insights" in input_data:
                    response = await self.generate_insights(input_data["sessions"])
                else:
                    raise AIServiceError("Unknown input data format")
            else:
                raise AIServiceError("Unsupported input data type")
            
            return response
        except Exception as e:
            await self.handle_api_error(e, "Gemini processing")
    
    async def generate_text(self, prompt: str) -> Dict[str, Any]:
        """Generate text response using the new Google GenAI SDK (2025)"""
        try:
            # Enhanced generation config for better Quran coaching responses
            generation_config = genai.types.GenerateContentConfig(
                temperature=0.3,  # Lower temperature for more consistent religious guidance
                top_p=0.8,
                top_k=40,
                max_output_tokens=2048,
                response_mime_type="text/plain",
                safety_settings=self.safety_settings
            )
            
            # Use the new Google GenAI SDK - now with native async support
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=[genai.types.Content(parts=[genai.types.Part(text=prompt)])],
                config=generation_config
            )
            
            return {
                "text": response.text,
                "usage": getattr(response, 'usage_metadata', {}),
                "safety_ratings": getattr(response, 'safety_ratings', []),
                "model_version": self.model_name,
                "sdk_version": "google-genai-2025"
            }
        except Exception as e:
            raise AIServiceError(f"Gemini text generation failed: {str(e)}")
    
    async def analyze_mistakes(self, mistakes: List[Dict[str, Any]]) -> AIAnalysisResult:
        """Analyze Quran recitation mistakes and provide insights"""
        try:
            # Construct analysis prompt
            mistakes_text = self._format_mistakes_for_analysis(mistakes)
            
            prompt = f"""
            Analyze the following Quran recitation mistakes and provide insights:

            {mistakes_text}

            Please provide analysis in the following JSON format:
            {{
                "mistake_patterns": [
                    {{
                        "pattern": "description of pattern",
                        "frequency": "high/medium/low",
                        "category": "pronunciation/memorization/tajweed"
                    }}
                ],
                "recommendations": [
                    {{
                        "action": "specific recommendation",
                        "priority": "high/medium/low",
                        "method": "practice method"
                    }}
                ],
                "focus_areas": ["area1", "area2"],
                "confidence_score": 0.85
            }}

            Focus on Islamic recitation principles and provide constructive guidance.
            """
            
            response = await self.generate_text(prompt)
            
            # Parse JSON response
            try:
                analysis_data = json.loads(response["text"])
                return AIAnalysisResult(
                    success=True,
                    data=analysis_data,
                    confidence=analysis_data.get("confidence_score", 0.8),
                    metadata={"model": self.model_name, "type": "mistake_analysis", "sdk": "google-genai-2025"}
                )
            except json.JSONDecodeError:
                # Fallback to structured text parsing
                return AIAnalysisResult(
                    success=True,
                    data={"analysis": response["text"]},
                    confidence=0.7,
                    metadata={"model": self.model_name, "type": "text_analysis", "sdk": "google-genai-2025"}
                )
                
        except Exception as e:
            return AIAnalysisResult(
                success=False,
                error=f"Mistake analysis failed: {str(e)}"
            )
    
    async def generate_insights(self, sessions: List[Dict[str, Any]]) -> AIAnalysisResult:
        """Generate coaching insights from session data"""
        try:
            # Format session data for analysis
            sessions_summary = self._format_sessions_for_analysis(sessions)
            
            prompt = f"""
            As an AI Quran memorization coach, analyze these practice sessions and provide personalized insights:

            {sessions_summary}

            Provide insights in JSON format:
            {{
                "overall_progress": "assessment of progress",
                "strengths": ["strength1", "strength2"],
                "areas_for_improvement": ["area1", "area2"],
                "personalized_recommendations": [
                    {{
                        "recommendation": "specific advice",
                        "rationale": "why this helps",
                        "implementation": "how to do it"
                    }}
                ],
                "review_schedule": {{
                    "next_review_date": "YYYY-MM-DD",
                    "priority_portions": ["portion1", "portion2"],
                    "suggested_frequency": "daily/weekly"
                }},
                "motivational_message": "encouraging message",
                "confidence_score": 0.9
            }}

            Base recommendations on Islamic learning principles and proven memorization techniques.
            """
            
            response = await self.generate_text(prompt)
            
            try:
                insights_data = json.loads(response["text"])
                return AIAnalysisResult(
                    success=True,
                    data=insights_data,
                    confidence=insights_data.get("confidence_score", 0.8),
                    metadata={"model": self.model_name, "type": "coaching_insights", "sdk": "google-genai-2025"}
                )
            except json.JSONDecodeError:
                return AIAnalysisResult(
                    success=True,
                    data={"insights": response["text"]},
                    confidence=0.7,
                    metadata={"model": self.model_name, "type": "text_insights", "sdk": "google-genai-2025"}
                )
                
        except Exception as e:
            return AIAnalysisResult(
                success=False,
                error=f"Insights generation failed: {str(e)}"
            )
    
    def _format_mistakes_for_analysis(self, mistakes: List[Dict[str, Any]]) -> str:
        """Format mistakes data for AI analysis"""
        formatted = []
        for i, mistake in enumerate(mistakes, 1):
            formatted.append(f"""
            Mistake {i}:
            - Location: {mistake.get('location', 'N/A')}
            - Category: {mistake.get('error_category', 'N/A')}
            - Subcategory: {mistake.get('error_subcategory', 'N/A')}
            - Details: {mistake.get('details', 'N/A')}
            - Severity: {mistake.get('severity_level', 1)}/5
            """)
        
        return "\n".join(formatted)
    
    def _format_sessions_for_analysis(self, sessions: List[Dict[str, Any]]) -> str:
        """Format session data for AI analysis"""
        formatted = []
        for i, session in enumerate(sessions, 1):
            formatted.append(f"""
            Session {i}:
            - Date: {session.get('timestamp', 'N/A')}
            - Duration: {session.get('duration', 'N/A')} minutes
            - Performance Score: {session.get('performance_score', 'N/A')}/100
            - Notes: {session.get('notes', 'N/A')}
            """)
        
        return "\n".join(formatted)

    async def categorize_mistake(self, mistake_description: str) -> AIAnalysisResult:
        """Categorize a single mistake using Gemini AI"""
        try:
            prompt = f"""
            Categorize this Quran recitation mistake:
            "{mistake_description}"

            Provide categorization in JSON format:
            {{
                "error_category": "pronunciation/memorization/tajweed/other",
                "error_subcategory": "specific subcategory",
                "severity_level": 1-5,
                "correction_method": "suggested correction approach",
                "confidence": 0.0-1.0
            }}

            Categories:
            - pronunciation: makhraj, sifat, clarity issues
            - memorization: word order, missing words, substitutions
            - tajweed: rules of recitation, timing, stops
            - other: other issues
            """
            
            response = await self.generate_text(prompt)
            
            try:
                category_data = json.loads(response["text"])
                return AIAnalysisResult(
                    success=True,
                    data=category_data,
                    confidence=category_data.get("confidence", 0.8),
                    metadata={"model": self.model_name, "type": "mistake_categorization", "sdk": "google-genai-2025"}
                )
            except json.JSONDecodeError:
                return AIAnalysisResult(
                    success=False,
                    error="Failed to parse categorization response"
                )
                
        except Exception as e:
            return AIAnalysisResult(
                success=False,
                error=f"Mistake categorization failed: {str(e)}"
            ) 