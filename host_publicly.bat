@echo off
echo ===================================================
echo   RoadSafe India - Host Public Website via Cloudflare
echo ===================================================
echo.
cd /d "%~dp0"

echo Starting local server if not already running...
start /b python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

timeout /t 3 >nul

echo Launching secure public HTTPS Cloudflare Tunnel...
cloudflared.exe tunnel --url http://127.0.0.1:8000
pause
