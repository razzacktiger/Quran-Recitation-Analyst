#!/usr/bin/env python3
"""
🗄️ Supabase Connection Test
Tests actual database connectivity and CRUD operations
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

def test_database_connection():
    """Test basic database connectivity"""
    print("🔄 Testing Supabase database connection...")
    
    try:
        from sqlmodel import create_engine, text
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ No DATABASE_URL found in environment")
            return False
        
        print(f"🔗 Connecting to: {database_url.split('@')[1] if '@' in database_url else 'database'}")
        
        # Create engine and test connection
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("✅ Database connection successful!")
                return True
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_table_creation():
    """Test creating tables"""
    print("🔄 Testing table creation...")
    
    try:
        from app.database import create_db_and_tables
        
        create_db_and_tables()
        print("✅ Tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def test_basic_crud():
    """Test basic CRUD operations"""
    print("🔄 Testing basic CRUD operations...")
    
    try:
        from app.database import get_db
        from app.models.sessions import Session, SessionCreate
        from sqlmodel import select
        
        # Test creating a session
        session_data = SessionCreate(
            user_id="test_user_connection",
            duration=15,
            performance_score=0.92
        )
        
        # This will test if our models work with the database
        with next(get_db()) as db:
            # Test insert
            new_session = Session.model_validate(session_data)
            new_session.id = None  # Let database assign ID
            db.add(new_session)
            db.commit()
            db.refresh(new_session)
            
            print(f"✅ Created session with ID: {new_session.id}")
            
            # Test select
            statement = select(Session).where(Session.user_id == "test_user_connection")
            found_session = db.exec(statement).first()
            
            if found_session:
                print(f"✅ Retrieved session: {found_session.user_id}")
            
            # Clean up test data
            db.delete(found_session)
            db.commit()
            print("✅ Cleaned up test data")
            
        return True
        
    except Exception as e:
        print(f"❌ CRUD operations failed: {e}")
        return False

def run_connection_tests():
    """Run all database connection tests"""
    print("🗄️ Supabase Connection Test Suite")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Table Creation", test_table_creation),
        ("Basic CRUD Operations", test_basic_crud),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 Test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 DATABASE TEST RESULTS")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 DATABASE TESTS: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 ALL DATABASE TESTS PASSED!")
        print("✅ Supabase connection working perfectly!")
        print("✅ Task 1.2.3 NOW COMPLETE!")
    else:
        print("⚠️ Some database tests failed.")
        print("💡 Check your .env file credentials")
    
    return passed == total

if __name__ == "__main__":
    run_connection_tests() 