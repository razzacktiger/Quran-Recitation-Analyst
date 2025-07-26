"""
Base AI service with common functionality and error handling
"""

import os
import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class AIServiceError(Exception):
    """Custom exception for AI service errors"""
    pass

class AIService(ABC):
    """Base class for AI services with common functionality"""
    
    def __init__(self):
        self.api_key = None
        self.rate_limit_retry = 3
        self.timeout = 30
    
    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input data and return results"""
        pass
    
    def validate_api_key(self, api_key: Optional[str]) -> str:
        """Validate and return API key"""
        if not api_key:
            raise AIServiceError("API key is required but not provided")
        return api_key
    
    async def handle_api_error(self, error: Exception, context: str = "") -> None:
        """Handle API errors with proper logging"""
        error_msg = f"AI Service Error {context}: {str(error)}"
        logger.error(error_msg)
        raise AIServiceError(error_msg)
    
    def validate_input(self, input_data: Any, required_fields: list = None) -> None:
        """Validate input data structure"""
        if required_fields:
            for field in required_fields:
                if field not in input_data:
                    raise AIServiceError(f"Required field '{field}' missing from input data")
    
    async def retry_on_failure(self, func, *args, **kwargs):
        """Retry function calls on failure"""
        last_error = None
        
        for attempt in range(self.rate_limit_retry):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.rate_limit_retry - 1:
                    break
                
                # Exponential backoff
                import asyncio
                await asyncio.sleep(2 ** attempt)
        
        raise AIServiceError(f"All retry attempts failed. Last error: {str(last_error)}")

class AIAnalysisResult:
    """Standardized result format for AI analysis"""
    
    def __init__(
        self, 
        success: bool,
        data: Dict[str, Any] = None,
        error: str = None,
        confidence: float = None,
        metadata: Dict[str, Any] = None
    ):
        self.success = success
        self.data = data or {}
        self.error = error
        self.confidence = confidence
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "confidence": self.confidence,
            "metadata": self.metadata
        } 