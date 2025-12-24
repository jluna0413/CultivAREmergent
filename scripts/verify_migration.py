import os
import sys
import requests
from flask import Flask
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from app.fastapi_main.main import app as fastapi_app_instance # Import the FastAPI app instance

def verify_flask_app():
    """Verifies the Flask application."""
    try:
        # Attempt to import the Flask app
        from cultivar_app import app as flask_app_instance
        print("✅ Flask app import OK")

        # Count Flask routes
        flask_routes = len(list(flask_app_instance.url_map.iter_rules()))
        print(f"✅ Flask app has {flask_routes} routes.")
        return True
    except Exception as e:
        print(f"❌ Flask app import or route count failed: {e}")
        return False

def verify_fastapi_app():
    """Verifies the FastAPI application."""
    try:
        # The FastAPI app instance is already imported as fastapi_app_instance
        print("✅ FastAPI app import OK")

        # Count FastAPI routes
        fastapi_routes = len(fastapi_app_instance.routes)
        print(f"✅ FastAPI app has {fastapi_routes} routes.")
        return True
    except Exception as e:
        print(f"❌ FastAPI app import or route count failed: {e}")
        return False

def verify_database_connection():
    """Verifies database connection for both sync and async (if configured)."""
    db_driver = os.getenv("CULTIVAR_DB_DRIVER", "sqlite")
    db_host = os.getenv("CULTIVAR_DB_HOST", "localhost")
    db_port = os.getenv("CULTIVAR_DB_PORT", "5432")
    db_user = os.getenv("CULTIVAR_DB_USER", "cultivar")
    db_password = os.getenv("CULTIVAR_DB_PASSWORD", "cultivar")
    db_name = os.getenv("CULTIVAR_DB_NAME", "cultivardb")

    if db_driver == "sqlite":
        db_url = "sqlite:///./test.db" # Using a test db for verification
    elif db_driver == "postgres":
        db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        print(f"⚠️ Unknown DB driver: {db_driver}")
        return False

    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print(f"✅ Sync DB connection ({db_driver}) OK")
        return True
    except Exception as e:
        print(f"❌ Sync DB connection ({db_driver}) failed: {e}")
        return False

def verify_static_and_templates():
    """Verifies the existence of static and templates directories."""
    critical_fails = 0
    if os.path.exists('app/static') and os.path.isdir('app/static'):
        print("✅ 'app/static' directory exists.")
    else:
        print("❌ 'app/static' directory is missing or not a directory.")
        critical_fails += 1

    if os.path.exists('app/templates') and os.path.isdir('app/templates'):
        print("✅ 'app/templates' directory exists.")
    else:
        print("❌ 'app/templates' directory is missing or not a directory.")
        critical_fails += 1
    return critical_fails == 0

def verify_environment_variables():
    """Verifies critical environment variables."""
    critical_fails = 0
    required_vars = ["SECRET_KEY", "CULTIVAR_DB_DRIVER"] # Add more as needed
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ Environment variable '{var}' is set.")
        else:
            print(f"❌ Environment variable '{var}' is NOT set.")
            critical_fails += 1
    return critical_fails == 0

def run_smoke_tests():
    """Runs basic smoke tests against running applications (assumes they are up)."""
    critical_fails = 0
    # Flask smoke test
    try:
        flask_port = os.getenv("CULTIVAR_PORT", "5000")
        response = requests.get(f"http://localhost:{flask_port}/")
        if response.status_code == 200:
            print(f"✅ Flask smoke test (GET /) OK. Status: {response.status_code}")
        else:
            print(f"❌ Flask smoke test (GET /) failed. Status: {response.status_code}")
            critical_fails += 1
    except requests.exceptions.ConnectionError:
        print("❌ Flask smoke test failed: Could not connect to Flask app. Is it running?")
        critical_fails += 1

    # FastAPI smoke test
    try:
        fastapi_port = os.getenv("FASTAPI_PORT", "8000")
        response = requests.get(f"http://localhost:{fastapi_port}/health")
        if response.status_code == 200:
            print(f"✅ FastAPI smoke test (GET /health) OK. Status: {response.status_code}")
        else:
            print(f"❌ FastAPI smoke test (GET /health) failed. Status: {response.status_code}")
            critical_fails += 1
    except requests.exceptions.ConnectionError:
        print("❌ FastAPI smoke test failed: Could not connect to FastAPI app. Is it running?")
        critical_fails += 1
    
    return critical_fails == 0

def main():
    print("--- Running CultivAR Migration Verification Script ---")
    
    overall_status = True
    report_content = "# Migration Status Report\n\n"

    print("\n--- Verifying Flask Application ---")
    flask_ok = verify_flask_app()
    report_content += f"- Flask Application: {'✅ OK' if flask_ok else '❌ FAILED'}\n"
    overall_status = overall_status and flask_ok

    print("\n--- Verifying FastAPI Application ---")
    fastapi_ok = verify_fastapi_app()
    report_content += f"- FastAPI Application: {'✅ OK' if fastapi_ok else '❌ FAILED'}\n"
    overall_status = overall_status and fastapi_ok

    print("\n--- Verifying Database Connection ---")
    db_ok = verify_database_connection()
    report_content += f"- Database Connection: {'✅ OK' if db_ok else '❌ FAILED'}\n"
    overall_status = overall_status and db_ok

    print("\n--- Verifying Static and Templates ---")
    static_templates_ok = verify_static_and_templates()
    report_content += f"- Static/Templates Directories: {'✅ OK' if static_templates_ok else '❌ FAILED'}\n"
    overall_status = overall_status and static_templates_ok

    print("\n--- Verifying Environment Variables ---")
    env_vars_ok = verify_environment_variables()
    report_content += f"- Environment Variables: {'✅ OK' if env_vars_ok else '❌ FAILED'}\n"
    overall_status = overall_status and env_vars_ok

    print("\n--- Running Smoke Tests (Assumes apps are running) ---")
    smoke_tests_ok = run_smoke_tests()
    report_content += f"- Smoke Tests: {'✅ OK' if smoke_tests_ok else '❌ FAILED'}\n"
    overall_status = overall_status and smoke_tests_ok

    print("\n--- Summary ---")
    if overall_status:
        print("🎉 All migration checks passed successfully!")
        report_content += "\n🎉 All migration checks passed successfully!\n"
    else:
        print("💔 Some migration checks failed. Please review the report above.")
        report_content += "\n💔 Some migration checks failed. Please review the report above.\n"
    
    with open("MIGRATION_STATUS.md", "w") as f:
        f.write(report_content)
    print("\nDetailed report written to MIGRATION_STATUS.md")

    sys.exit(0 if overall_status else 1)

if __name__ == "__main__":
    main()
