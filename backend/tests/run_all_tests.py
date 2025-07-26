#!/usr/bin/env python3
"""
🎯 Master Test Runner
Runs all test suites to verify 2025 dependency updates
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    """Run all test suites"""
    print("🚀 AI-Powered Quran Coach - Complete Test Suite")
    print("🎯 Verifying all 2025 dependency updates")
    print("=" * 70)
    
    all_passed = True
    
    try:
        # Run dependency tests
        print("\n" + "🔧 DEPENDENCY TESTS".center(70, "="))
        from test_2025_dependencies import run_manual_tests
        dep_passed = run_manual_tests()
        all_passed = all_passed and dep_passed
        
        print("\n" + "🌐 API INTEGRATION TESTS".center(70, "="))
        from test_api_endpoints import run_api_tests
        api_passed = run_api_tests()
        all_passed = all_passed and api_passed
        
    except Exception as e:
        print(f"💥 Test runner error: {e}")
        all_passed = False
    
    # Final summary
    print("\n" + "🏁 FINAL RESULTS".center(70, "="))
    
    if all_passed:
        print("🎉 🎉 🎉 ALL TESTS PASSED! 🎉 🎉 🎉")
        print()
        print("✅ Your 2025 dependency updates are working perfectly!")
        print("✅ Google GenAI SDK migration successful")
        print("✅ OpenAI AsyncClient working")
        print("✅ FastAPI 0.115.6 working")
        print("✅ Pydantic 2.11.7 working")
        print("✅ SQLModel JSON fix working")
        print("✅ All API endpoints accessible")
        print()
        print("🚀 READY TO COMMIT TO GITHUB!")
        print("=" * 70)
        return 0
    else:
        print("❌ Some tests failed - check output above")
        print("⚠️ Fix issues before committing")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 