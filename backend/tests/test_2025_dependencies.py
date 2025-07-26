#!/usr/bin/env python3
"""
🧪 Test Suite for 2025 Dependency Updates
Tests all critical functionality after migrating to latest packages:
- Google GenAI SDK (replaced deprecated google-generativeai)
- OpenAI AsyncClient 
- FastAPI 0.115.6
- Pydantic 2.11.7
- SQLModel 0.0.24
- All other updated dependencies
"""

import asyncio
import sys
import os
import pytest
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Test2025Dependencies:
    """Test class for all 2025 dependency updates"""
    
    def test_google_genai_sdk_import(self):
        """Test the NEW Google GenAI SDK imports correctly"""
        print("🔄 Testing Google GenAI SDK import...")
        
        try:
            from google import genai
            print("✅ Google GenAI SDK import successful")
            assert True
        except ImportError as e:
            print(f"❌ Google GenAI SDK import failed: {e}")
            assert False, f"Google GenAI SDK import failed: {e}"
    
    def test_openai_async_client_import(self):
        """Test the latest OpenAI AsyncClient imports correctly"""
        print("🔄 Testing OpenAI AsyncClient import...")
        
        try:
            from openai import AsyncOpenAI
            print("✅ OpenAI AsyncClient import successful")
            assert True
        except ImportError as e:
            print(f"❌ OpenAI AsyncClient import failed: {e}")
            assert False, f"OpenAI AsyncClient import failed: {e}"
    
    def test_fastapi_models_import(self):
        """Test all FastAPI models with new Pydantic/SQLModel versions"""
        print("🔄 Testing FastAPI models...")
        
        try:
            from app.models.sessions import Session, SessionCreate, SessionRead, SessionUpdate
            from app.models.insights import Insight, InsightCreate, InsightRead, InsightUpdate  
            from app.models.mistakes import Mistake, MistakeCreate, MistakeRead, MistakeUpdate
            from app.models.portion_details import PortionDetail, PortionDetailCreate
            print("✅ All database models import successfully")
            assert True
        except ImportError as e:
            print(f"❌ Model import failed: {e}")
            assert False, f"Model import failed: {e}"
    
    def test_pydantic_model_creation(self):
        """Test Pydantic model creation with new version"""
        print("🔄 Testing Pydantic model creation...")
        
        try:
            from app.models.sessions import SessionCreate
            
            session_data = {
                "user_id": "test_user_123",
                "duration": 30,
                "performance_score": 0.85
            }
            session = SessionCreate(**session_data)
            
            assert session.user_id == "test_user_123"
            assert session.duration == 30
            assert session.performance_score == 0.85
            
            print("✅ Pydantic SessionCreate model works correctly")
            assert True
            
        except Exception as e:
            print(f"❌ Pydantic model creation failed: {e}")
            assert False, f"Pydantic model creation failed: {e}"
    
    def test_json_field_sqlmodel_fix(self):
        """Test the critical JSON field fix for SQLModel compatibility"""
        print("🔄 Testing JSON field SQLModel fix...")
        
        try:
            from app.models.insights import InsightCreate
            
            insight_data = {
                "user_id": "test_user_123",
                "summary": "Test insight with JSON field",
                "next_actions": {
                    "review": ["Surah Al-Fatiha", "Surah Al-Baqarah"],
                    "practice": "Focus on Tajweed rules",
                    "schedule": {"next_session": "2025-01-26", "frequency": "daily"}
                },
                "confidence_score": 0.92
            }
            
            insight = InsightCreate(**insight_data)
            
            assert insight.user_id == "test_user_123"
            assert insight.next_actions["review"] == ["Surah Al-Fatiha", "Surah Al-Baqarah"]
            assert insight.confidence_score == 0.92
            
            print("✅ JSON field works correctly with SQLModel fix")
            assert True
            
        except Exception as e:
            print(f"❌ JSON field test failed: {e}")
            assert False, f"JSON field test failed: {e}"
    
    def test_ai_service_imports(self):
        """Test our custom AI service classes import correctly"""
        print("🔄 Testing AI service imports...")
        
        try:
            from app.services.gemini_service import GeminiService
            from app.services.whisper_service import WhisperService
            from app.services.ai_service import AIService, AIAnalysisResult
            print("✅ All AI service classes import successfully")
            assert True
        except ImportError as e:
            print(f"❌ AI service import failed: {e}")
            assert False, f"AI service import failed: {e}"
    
    def test_fastapi_app_import(self):
        """Test FastAPI app imports with all updated dependencies"""
        print("🔄 Testing FastAPI app import...")
        
        try:
            from app.main import app
            assert app is not None
            print("✅ FastAPI app imports successfully")
            assert True
        except ImportError as e:
            print(f"❌ FastAPI app import failed: {e}")
            assert False, f"FastAPI app import failed: {e}"
    
    def test_database_models_table_creation(self):
        """Test database models can be defined (without actual DB connection)"""
        print("🔄 Testing database model definitions...")
        
        try:
            from app.models.sessions import Session
            from app.models.insights import Insight
            from app.models.mistakes import Mistake
            
            # Test that table definitions exist
            assert hasattr(Session, '__tablename__')
            assert hasattr(Insight, '__tablename__')
            assert hasattr(Mistake, '__tablename__')
            
            assert Session.__tablename__ == "sessions"
            assert Insight.__tablename__ == "insights"
            assert Mistake.__tablename__ == "mistakes"
            
            print("✅ Database model table definitions work correctly")
            assert True
            
        except Exception as e:
            print(f"❌ Database model test failed: {e}")
            assert False, f"Database model test failed: {e}"
    
    @pytest.mark.asyncio
    async def test_ai_service_initialization(self):
        """Test AI services can be initialized (without real API keys)"""
        print("🔄 Testing AI service initialization...")
        
        from app.services.gemini_service import GeminiService
        from app.services.whisper_service import WhisperService
        
        # Test that services fail gracefully without API keys
        try:
            gemini = GeminiService()
            print("⚠️ GeminiService initialized - API key might be present")
        except Exception as e:
            if "API key" in str(e):
                print("✅ GeminiService correctly requires API key")
            else:
                print(f"❌ Unexpected GeminiService error: {e}")
                assert False, f"Unexpected GeminiService error: {e}"
        
        try:
            whisper = WhisperService()
            print("⚠️ WhisperService initialized - API key might be present")
        except Exception as e:
            if "API key" in str(e):
                print("✅ WhisperService correctly requires API key")
            else:
                print(f"❌ Unexpected WhisperService error: {e}")
                assert False, f"Unexpected WhisperService error: {e}"
        
        assert True

def run_manual_tests():
    """Run tests manually without pytest for quick verification"""
    print("🚀 AI-Powered Quran Coach - 2025 Dependency Test Suite")
    print("=" * 60)
    
    test_instance = Test2025Dependencies()
    
    # List of test methods
    test_methods = [
        ("Google GenAI SDK Import", test_instance.test_google_genai_sdk_import),
        ("OpenAI AsyncClient Import", test_instance.test_openai_async_client_import),
        ("FastAPI Models Import", test_instance.test_fastapi_models_import),
        ("Pydantic Model Creation", test_instance.test_pydantic_model_creation),
        ("JSON Field SQLModel Fix", test_instance.test_json_field_sqlmodel_fix),
        ("AI Service Imports", test_instance.test_ai_service_imports),
        ("FastAPI App Import", test_instance.test_fastapi_app_import),
        ("Database Model Definitions", test_instance.test_database_models_table_creation),
    ]
    
    results = []
    
    for test_name, test_method in test_methods:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        try:
            test_method()
            results.append((test_name, True))
        except Exception as e:
            print(f"💥 Test failed: {e}")
            results.append((test_name, False))
    
    # Test async method separately
    print(f"\n📋 AI Service Initialization (Async)")
    print("-" * 40)
    try:
        asyncio.run(test_instance.test_ai_service_initialization())
        results.append(("AI Service Initialization", True))
    except Exception as e:
        print(f"💥 Async test failed: {e}")
        results.append(("AI Service Initialization", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 OVERALL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your 2025 dependency updates are working perfectly!")
        print("✅ Safe to commit to GitHub!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    run_manual_tests() 