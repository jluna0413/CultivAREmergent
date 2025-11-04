"""
Test script to validate Flask async session management implementation.

This test validates that the FlaskAsyncSessionManager and related utilities
work correctly for async operations in Flask blueprints.
"""

import asyncio
import sys
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from utils.async_flask_helpers import FlaskAsyncSessionManager, get_flask_async_session
from handlers.clone_handlers_async import get_clones, get_clone_statistics


async def test_flask_async_session_manager():
    """Test FlaskAsyncSessionManager context manager."""
    print("Testing FlaskAsyncSessionManager...")
    
    try:
        async with FlaskAsyncSessionManager() as session:
            # Test that we get a valid async session
            assert session is not None
            print("✅ FlaskAsyncSessionManager creates valid session")
            
            # Test basic query functionality
            stats = await get_clone_statistics(session)
            print(f"✅ Successfully queried clone statistics: {stats}")
            
            # Test get_clones function
            clones = await get_clones(session)
            print(f"✅ Successfully retrieved {len(clones)} clones")
            
        print("✅ FlaskAsyncSessionManager test passed")
        return True
        
    except Exception as e:
        print(f"❌ FlaskAsyncSessionManager test failed: {e}")
        return False


async def test_manual_async_session():
    """Test manual async session creation."""
    print("\nTesting manual async session creation...")
    
    try:
        session = await get_flask_async_session()
        
        # Test basic functionality
        stats = await get_clone_statistics(session)
        print(f"✅ Manual session - Clone stats: {stats}")
        
        # Clean up
        await session.close()
        print("✅ Manual session test passed")
        return True
        
    except Exception as e:
        print(f"❌ Manual session test failed: {e}")
        return False


async def test_session_context_error_handling():
    """Test error handling in session context."""
    print("\nTesting session context error handling...")
    
    try:
        async with FlaskAsyncSessionManager() as session:
            # Test error handling (try to query non-existent data)
            try:
                # This should handle gracefully
                stats = await get_clone_statistics(session)
                print("✅ Error handling test passed")
                return True
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Session context error handling failed: {e}")
        return False


async def main():
    """Run all async session tests."""
    print("🚀 Starting Flask Async Session Management Tests")
    print("=" * 60)
    
    tests = [
        test_flask_async_session_manager,
        test_manual_async_session,
        test_session_context_error_handling,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = await test()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All async session management tests passed!")
        return True
    else:
        print("❌ Some tests failed - async session management needs fixes")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)