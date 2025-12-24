@echo off
REM 🚀 CultivAR Real-World Validation Quick Start Script (Windows)
REM This script launches all necessary services for comprehensive validation

echo 🚀 Starting CultivAR Real-World Validation Environment...

REM Navigate to project root
cd a:/dev/CultivAREmergant

REM Check if we're in the right directory
if not exist "run_fastapi.py" (
    echo ❌ Error: Not in project root directory
    echo Please navigate to a:/dev/CultivAREmergant first
    pause
    exit /b 1
)

echo ✅ Project root verified

REM Function to start FastAPI backend in background
:start_fastapi
echo 🔧 Starting FastAPI backend...
start /b python run_fastapi.py
echo FastAPI backend started
timeout /t 3 /nobreak >nul
goto :eof

REM Function to start Flask web interface (optional)
:start_flask
echo 🌐 Starting Flask web interface (optional)...
start /b python run_flask.py
echo Flask web interface started
timeout /t 2 /nobreak >nul
goto :eof

REM Function to verify services are running
:verify_services
echo 🔍 Verifying services...

REM Check FastAPI
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ FastAPI backend is running
) else (
    echo ❌ FastAPI backend not responding
    goto :service_error
)

REM Check Flask (optional)
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Flask web interface is running
) else (
    echo ⚠️  Flask web interface not responding (this is optional)
)

goto :eof

:service_error
echo Please start the backend services first
pause
exit /b 1

REM Function to launch Flutter app
:launch_flutter
echo 📱 Launching Flutter app...

cd flutter_app

REM Check if Flutter is available
flutter --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Flutter not found. Please install Flutter first.
    echo Visit: https://flutter.dev/docs/get-started/install
    pause
    exit /b 1
)

REM Get Flutter packages
echo 📦 Getting Flutter dependencies...
flutter pub get

REM Launch Flutter app in web mode (recommended for testing)
echo 🌐 Launching Flutter web app...
echo The app will open in your default browser
echo Press Ctrl+C to stop the Flutter app

flutter run -d chrome --web-renderer canvaskit
goto :eof

REM Function to run validation tests
:run_validation_tests
echo 🧪 Running validation tests...

cd ..

REM Install dependencies if needed
python -c "import pytest, httpx, jwt" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing Python dependencies...
    pip install pytest httpx jwt requests
)

echo 🔐 Running security validation...
python tests/security/security_validation_framework.py

echo 🔧 Running IoT integration tests...
python tests/iot/iot_integration_validation.py

echo 🛡️ Running OWASP ZAP scan (requires Docker)...
python scripts/owasp_zap_scanner.py --scan

pause
goto :eof

REM Main menu
:main_menu
echo.
echo Select an option:
echo 1. Start FastAPI backend only
echo 2. Start FastAPI + Flask (full stack)
echo 3. Launch Flutter app (requires backend running)
echo 4. Run all validation tests
echo 5. Complete setup: Start backend + Launch Flutter
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto :start_fastapi
if "%choice%"=="2" goto :start_fastapi_and_flask
if "%choice%"=="3" goto :launch_flutter_check_backend
if "%choice%"=="4" goto :run_validation_tests
if "%choice%"=="5" goto :complete_setup
if "%choice%"=="6" goto :exit
echo ❌ Invalid choice
goto :main_menu

:start_fastapi_and_flask
call :start_fastapi
call :start_flask
call :verify_services
goto :main_menu

:launch_flutter_check_backend
call :verify_services
if %errorlevel% equ 0 (
    call :launch_flutter
) else (
    echo ❌ Please start the backend first (option 1 or 2)
    goto :main_menu
)

:complete_setup
call :start_fastapi_and_flask
timeout /t 5 /nobreak >nul
call :launch_flutter
goto :eof

:exit
echo 👋 Goodbye!
pause
exit /b 0

REM Start the main menu
goto :main_menu