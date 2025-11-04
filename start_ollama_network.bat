@echo off
REM Ollama Network Server Startup Script
REM This script starts Ollama configured for network access on 0.0.0.0:11434

echo Starting Ollama with network access enabled...
echo.
echo Configuration: OLLAMA_HOST=0.0.0.0:11434
echo Port: 11434
echo Network IP: 192.168.1.204
echo.
echo Note: You may need to run this as Administrator to modify firewall rules
echo.

REM Check if Ollama is already running
tasklist /fi "imagename eq ollama.exe" 2>NUL | find /i /n "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Ollama is already running. Stopping existing instances...
    taskkill /f /im ollama.exe 2>NUL
    taskkill /f /im "ollama app.exe" 2>NUL
    timeout /t 2 /nobreak >NUL
)

echo Starting Ollama server...
set OLLAMA_HOST=0.0.0.0:11434
ollama serve

pause