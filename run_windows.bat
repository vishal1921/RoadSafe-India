@echo off
title RoadSafe India — AI Road Safety Intelligence Platform
color 0B

echo =========================================================================
echo       ROADSAFE INDIA: AI ROAD SAFETY INTELLIGENCE PLATFORM
echo          Problem Statement No. 3 - Transport: RoadSafe India
echo                   National Level Hackathon Project
echo =========================================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH.
    echo Please install Python 3.10+ from python.org and add to PATH.
    pause
    exit /b 1
)
python --version

echo.
echo [2/3] Verifying dependencies...
pip install -r backend\requirements.txt --quiet --disable-pip-version-check

echo.
echo [3/3] Checking network port availability...
set PORT=8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo [NOTE] Port 8000 is occupied by PID %%a. Releasing port...
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 1 /nobreak >nul 2>&1

netstat -aon | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Port 8000 remains occupied. Automatically routing to fallback port 8008.
    set PORT=8008
)

echo.
echo =========================================================================
echo   Command Center Dashboard : http://127.0.0.1:%PORT%
echo   Interactive Swagger Docs : http://127.0.0.1:%PORT%/docs
echo   Alternative ReDoc Specs  : http://127.0.0.1:%PORT%/redoc
echo =========================================================================
echo Press Ctrl+C to terminate the server.
echo.

python -m uvicorn backend.main:app --host 127.0.0.1 --port %PORT% --reload
pause
