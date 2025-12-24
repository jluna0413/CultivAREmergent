
import pytest

def test_imports():
    print("\nSTART DEBUG")
    try:
        from app.database import get_db
        print("PASS: app.database")
    except Exception as e:
        print(f"FAIL: app.database - {e}")

    try:
        from app.fastapi_app.dependencies import require_login
        print("PASS: app.fastapi_app.dependencies")
    except Exception as e:
        print(f"FAIL: app.fastapi_app.dependencies - {e}")

    try:
        from app.models_async.breeders import MarketplaceBreeder
        print("PASS: app.models_async.breeders")
    except Exception as e:
        print(f"FAIL: app.models_async.breeders - {e}")

    try:
        from app.services.hypergraph_service import HypergraphService
        print("PASS: app.services.hypergraph_service")
    except Exception as e:
        print(f"FAIL: app.services.hypergraph_service - {e}")
        
    try:
        from app.fastapi_app.routers import marketplace_breeders
        print("PASS: app.fastapi_app.routers.marketplace_breeders")
    except Exception as e:
        print(f"FAIL: app.fastapi_app.routers.marketplace_breeders - {e}")
    print("END DEBUG")
