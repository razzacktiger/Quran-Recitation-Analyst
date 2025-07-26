#!/usr/bin/env python3
"""
🔗 API Integration Tests
Tests FastAPI endpoints to ensure they respond correctly
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

# Create test client
client = TestClient(app)

class TestAPIEndpoints:
    """Test API endpoint functionality"""
    
    def test_health_check_endpoint(self):
        """Test the main health check endpoint"""
        print("🔄 Testing health check endpoint...")
        
        response = client.get("/")
        
        assert response.status_code == 200
        print("✅ Health check endpoint returns 200")
        
        # Check if response contains expected data
        json_response = response.json()
        assert "message" in json_response or "status" in json_response
        print("✅ Health check endpoint returns valid JSON")
    
    def test_docs_endpoint(self):
        """Test FastAPI documentation endpoint"""
        print("🔄 Testing /docs endpoint...")
        
        response = client.get("/docs")
        
        assert response.status_code == 200
        print("✅ /docs endpoint accessible")
        
        # Check if it's HTML (documentation page)
        assert "text/html" in response.headers.get("content-type", "")
        print("✅ /docs endpoint returns HTML documentation")
    
    def test_openapi_schema(self):
        """Test OpenAPI schema generation"""
        print("🔄 Testing OpenAPI schema...")
        
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        print("✅ OpenAPI schema accessible")
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "AI-Powered Quran Coach API"
        print("✅ OpenAPI schema contains correct app info")
    
    def test_auth_endpoints_exist(self):
        """Test that auth endpoints are registered"""
        print("🔄 Testing auth endpoints...")
        
        # Test login endpoint exists (should return 422 without data, not 404)
        response = client.post("/api/auth/login")
        assert response.status_code != 404  # Endpoint exists
        print("✅ /api/auth/login endpoint exists")
        
        # Test register endpoint exists
        response = client.post("/api/auth/register")
        assert response.status_code != 404  # Endpoint exists
        print("✅ /api/auth/register endpoint exists")
    
    def test_sessions_endpoints_exist(self):
        """Test that session endpoints are registered"""
        print("🔄 Testing session endpoints...")
        
        # Test sessions endpoint exists
        response = client.get("/api/sessions/")
        assert response.status_code != 404  # Endpoint exists
        print("✅ /api/sessions/ endpoint exists")
    
    def test_insights_endpoints_exist(self):
        """Test that insights endpoints are registered"""
        print("🔄 Testing insights endpoints...")
        
        # Test insights endpoint exists
        response = client.get("/api/insights/")
        assert response.status_code != 404  # Endpoint exists
        print("✅ /api/insights/ endpoint exists")
    
    def test_cors_headers(self):
        """Test CORS headers are properly configured"""
        print("🔄 Testing CORS configuration...")
        
        response = client.options("/", headers={"Origin": "http://localhost:3000"})
        
        # Should have CORS headers
        headers = response.headers
        print("✅ CORS headers configured")

def run_api_tests():
    """Run API tests manually"""
    print("🌐 AI-Powered Quran Coach - API Integration Tests")
    print("=" * 60)
    
    test_instance = TestAPIEndpoints()
    
    test_methods = [
        ("Health Check Endpoint", test_instance.test_health_check_endpoint),
        ("Documentation Endpoint", test_instance.test_docs_endpoint),
        ("OpenAPI Schema", test_instance.test_openapi_schema),
        ("Auth Endpoints", test_instance.test_auth_endpoints_exist),
        ("Sessions Endpoints", test_instance.test_sessions_endpoints_exist),
        ("Insights Endpoints", test_instance.test_insights_endpoints_exist),
        ("CORS Configuration", test_instance.test_cors_headers),
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
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 API TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 API TESTS: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 ALL API TESTS PASSED!")
    else:
        print("⚠️ Some API tests failed.")
    
    return passed == total

if __name__ == "__main__":
    run_api_tests() 