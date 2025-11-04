@echo off
echo Starting FastAPI CultivAR Application on port 5001...

REM Kill any existing processes on port 5001
echo Checking if port 5001 is already in use...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5001') do (
    echo Killing process with PID: %%a
    taskkill /F /PID %%a
)

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found at .venv
)

REM Set environment variables
set CULTIVAR_PORT=5001
set DEBUG=true
if "%SECRET_KEY%"=="" (
    for /f "delims=" %%i in ('powershell -Command "[System.Web.Security.Membership]::GeneratePassword(32,4)"') do set SECRET_KEY=%%i
    echo Generated secure development key.
)

REM Start FastAPI with uvicorn
echo Starting FastAPI application...
echo Server will be available at http://localhost:5001
uvicorn fastapi_app:app --host 0.0.0.0 --port 5001 --reload

pause
