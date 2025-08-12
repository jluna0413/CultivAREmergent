@echo off
echo Starting CultivAR on port 5000...

REM Create necessary directories
if not exist data mkdir data
if not exist uploads mkdir uploads
if not exist uploads\plants mkdir uploads\plants
if not exist uploads\streams mkdir uploads\streams
if not exist uploads\logos mkdir uploads\logos
if not exist logs mkdir logs

REM Set environment variables
set CULTIVAR_PORT=5000

REM Kill any existing processes on port 5000
echo Checking if port 5000 is already in use...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    echo Killing process with PID: %%a
    taskkill /F /PID %%a
)

REM Run the simplified application
echo Starting Simplified CultivAR on port 5000...
python simple_app.py

pause
