#!/usr/bin/env python3
"""
Simple test script to verify strain->cultivar migration is working correctly
"""
import os
import sys

# Set environment variable before importing app
os.environ['SECRET_KEY'] = 'test-secret-key-for-migration-test'

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")
    
    try:
        # Test FastAPI app import
        from app.fastapi_app import app
        print("✓ FastAPI app imported successfully")
        
        # Test cultivars router import
        from app.fastapi_app.routers import cultivars
        print("✓ Cultivars router imported successfully")
        
        # Test breeders router import
        from app.fastapi_app.routers import breeders
        print("✓ Breeder router imported successfully")
        
        # Test models imports
        from app.fastapi_app.models import cultivars as cultivars_models
        print("✓ Cultivar models imported successfully")
        
        from app.fastapi_app.models import breeders as breeders_models
        print("✓ Breeder models imported successfully")
        
        # Test legacy strains router still exists
        from app.fastapi_app.routers import strains
        print("✓ Legacy strains router still imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"X Import error: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"X Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_router_mounting():
    """Test that routers are properly mounted"""
    print("\nTesting router mounting...")
    
    try:
        from app.fastapi_app import app
        
        # Get all routes
        routes = app.routes
        
        # Find cultivar/strain routes
        cultivar_routes = [route for route in routes if '/api/v1/cultivars' in route.path]
        legacy_strain_routes = [route for route in routes if '/api/v1/strains' in route.path]
        
        print(f"✓ Found {len(cultivar_routes)} primary cultivar routes")
        print(f"✓ Found {len(legacy_strain_routes)} legacy strain routes")
        
        # Show some examples
        print("\nPrimary cultivars routes:")
        for route in cultivar_routes[:3]:
            print(f"  - {route.methods} {route.path}")
            
        print("\nLegacy strains routes:")
        for route in legacy_strain_routes[:3]:
            print(f"  - {route.methods} {route.path} (legacy)")
        
        return True
        
    except Exception as e:
        print(f"X Router mounting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_breeder_alignment():
    """Test that breeder responses use cultivar terminology"""
    print("\nTesting breeder terminology alignment...")
    
    try:
        from app.fastapi_app.models.breeders import BreederResponse, BreederStats
        
        # Check BreederResponse fields
        actual_fields = list(BreederResponse.model_fields.keys())
        
        print(f"✓ BreederResponse fields: {actual_fields}")
        
        if 'cultivar_count' in actual_fields:
            print("✓ BreederResponse uses 'cultivar_count' field")
        else:
            print("X BreederResponse missing 'cultivar_count' field")
            return False
            
        # Check BreederStats fields
        stats_fields = list(BreederStats.model_fields.keys())
        print(f"✓ BreederStats fields: {stats_fields}")
        
        if 'total_cultivars_from_top_breeder' in stats_fields:
            print("✓ BreederStats uses 'total_cultivars_from_top_breeder' field")
        else:
            print("X BreederStats missing 'total_cultivars_from_top_breeder' field")
            return False
        
        return True
        
    except Exception as e:
        print(f"X Breeder alignment test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cultivar_models():
    """Test that cultivar models exist and are correctly named"""
    print("\nTesting cultivar models...")
    
    try:
        from app.fastapi_app.models.cultivars import (
            CultivarBase, 
            CultivarCreate, 
            CultivarUpdate, 
            CultivarResponse,
            CultivarListResponse,
            CultivarFilters,
            CultivarStats
        )
        
        print("✓ All cultivar model classes imported successfully")
        
        # Check that they're not still named with 'Strain'
        model_names = [
            'CultivarBase', 'CultivarCreate', 'CultivarUpdate', 
            'CultivarResponse', 'CultivarListResponse', 
            'CultivarFilters', 'CultivarStats'
        ]
        
        for name in model_names:
            if 'Strain' in name:
                print(f"X Model {name} still contains 'Strain'")
                return False
        
        print("✓ All models use 'Cultivar' terminology")
        return True
        
    except Exception as e:
        print(f"X Cultivar models test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("Testing Strain->Cultivar Migration")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Router Mounting Tests", test_router_mounting),
        ("Breeder Alignment Tests", test_breeder_alignment),
        ("Cultivar Models Tests", test_cultivar_models)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"X {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Migration appears successful.")
        return True
    else:
        print("Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)