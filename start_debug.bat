@echo off
REM Set environment variables for debug mode
set SECRET_KEY=your-secret-key-for-development
set DEBUG=true
set CULTIVAR_PORT=5000

REM Debug: Show environment variables to verify they're set
echo SECRET_KEY: %SECRET_KEY%
echo DEBUG: %DEBUG%
echo CULTIVAR_PORT: %CULTIVAR_PORT%

REM Start the Flask application
python cultivar_app.py
