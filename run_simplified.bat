@echo off
echo Starting Simplified CultivAR on port 4200...

REM Kill any existing processes on port 4200
echo Checking if port 4200 is already in use...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :4200') do (
    echo Killing process with PID: %%a
    taskkill /F /PID %%a
)

REM Run the simplified application
echo Starting Simplified CultivAR on port 4200...
python simple_app.py

pause
