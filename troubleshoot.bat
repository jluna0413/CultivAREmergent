@echo off
echo Running CultivAR in debug mode with detailed output...

REM Set environment variables
set CULTIVAR_PORT=5000
set FLASK_DEBUG=1

REM Create log directory if it doesn't exist
if not exist logs mkdir logs

REM Run the application with output redirected to a log file
echo Starting application on port 5000...
python main.py > logs\startup.log 2>&1

echo Application has stopped. Check logs\startup.log for details.
pause
