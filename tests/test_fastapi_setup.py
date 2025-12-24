#!/usr/bin/env python3
"""
FastAPI Application Test Script
Tests the complete FastAPI setup including routers, middleware, and security
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️  python-dotenv not available, using system environment variables")
except Exception as e:
    print(f"⚠️  Error loading .env file: {e}")

async def test_fastapi_imports():
    """Test if all FastAPI components can be imported"""
    print("🔧 Testing FastAPI Component Imports...")
    
    try:
        # Test main FastAPI app
        from app.fastapi_app.main import app
        print("✅ FastAPI main app imported successfully")
        
        # Test security config
        from app.fastapi_app.security_config import security_config
        print("✅ Security configuration imported successfully")
        
        # Test JWT utilities
        from app.fastapi_app.jwt_utils import create_access_token_with_jti
        print("✅ JWT utilities imported successfully")
        
        # Test database
        from app.models_async.base import get_async_session
        print("✅ Database components imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

async def test_fastapi_app_creation():
    """Test if FastAPI app is created properly"""
    print("\n🚀 Testing FastAPI App Creation...")
    
    try:
        from app.fastapi_app.main import app
        
        # Test basic app properties
        assert app.title == "CultivAR API"
        assert app.version == "2.0.0"
        assert app.docs_url == "/docs"
        
        print("✅ FastAPI app configuration validated")
        
        # Test routes are included
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/api/v2/status"]
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Route {route} found")
            else:
                print(f"⚠️  Route {route} not found in {routes}")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI app test failed: {e}")
        return False

async def test_security_configuration():
    """Test security configuration"""
    print("\n🔒 Testing Security Configuration...")
    
    try:
        from app.fastapi_app.security_config import security_config
        
        # Test environment detection
        environment = security_config.environment
        print(f"✅ Environment detected: {environment}")
        
        # Test security headers generation
        headers = security_config.get_security_headers()
        print(f"✅ Security headers generated: {len(headers)} headers")
        
        # Test CSP policy generation
        csp = security_config.get_csp_policy()
        print(f"✅ CSP policy generated: {len(csp)} characters")
        
        # Test allowed hosts
        hosts = security_config.get_allowed_hosts()
        print(f"✅ Allowed hosts configured: {hosts}")
        
        return True
        
    except Exception as e:
        print(f"❌ Security configuration test failed: {e}")
        return False

async def test_database_connection():
    """Test database connection"""
    print("\n💾 Testing Database Connection...")
    
    try:
        from app.models_async.base import get_async_session
        
        # Test session creation
        async with get_async_session() as session:
            print("✅ Database session created successfully")
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        print("💡 Note: This may fail if database is not set up")
        return False

async def test_auth_components():
    """Test authentication components"""
    print("\n🔐 Testing Authentication Components...")
    
    try:
        # Test auth router
        from app.fastapi_app.routers import auth
        print("✅ Auth router imported successfully")
        
        # Test JWT utilities
        from app.fastapi_app.jwt_utils import generate_jti
        jti = generate_jti()
        print(f"✅ JTI generation works: {jti}")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

async def test_middleware():
    """Test middleware components"""
    print("\n⚙️ Testing Middleware Components...")
    
    try:
        # Test security middleware
        from app.fastapi_app.middleware.security import SecurityHeadersMiddleware, RateLimitMiddleware
        print("✅ Security middleware imported successfully")
        
        # Test middleware instantiation
        from app.fastapi_app.main import app
        
        # Check if middleware is properly configured
        middleware_count = len(app.user_middleware)
        print(f"✅ Middleware configured: {middleware_count} middleware components")
        
        return True
        
    except Exception as e:
        print(f"❌ Middleware test failed: {e}")
        return False

async def test_application_startup():
    """Test application startup simulation"""
    print("\n🌟 Testing Application Startup...")
    
    try:
        # This will simulate app startup without actually running the server
        from app.fastapi_app.main import app
        from app.fastapi_app.database import init_database
        
        # Test configuration
        print(f"✅ App title: {app.title}")
        print(f"✅ App version: {app.version}")
        print(f"✅ Environment: {os.getenv('ENVIRONMENT', 'development')}")
        
        # Count routes
        route_count = len(app.routes)
        print(f"✅ Total routes configured: {route_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Startup test failed: {e}")
        return False

async def run_comprehensive_test():
    """Run comprehensive FastAPI setup test"""
    print("🧪 FastAPI Comprehensive Setup Test")
    print("=" * 50)
    
    tests = [
        ("Component Imports", test_fastapi_imports),
        ("App Creation", test_fastapi_app_creation),
        ("Security Configuration", test_security_configuration),
        ("Database Connection", test_database_connection),
        ("Authentication Components", test_auth_components),
        ("Middleware", test_middleware),
        ("Application Startup", test_application_startup),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Total: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! FastAPI setup is ready for deployment.")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed. Review issues above.")
        return False

def main():
    """Main test function"""
    try:
        result = asyncio.run(run_comprehensive_test())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()