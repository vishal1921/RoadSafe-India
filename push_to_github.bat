@echo off
echo ===================================================
echo   RoadSafe India - Push to GitHub Repository
echo   Remote: https://github.com/nandeshmontfort-bot/Team_015.git
echo ===================================================
echo.
cd /d "%~dp0"

echo Current Git Status:
git status
echo.
echo Pushing local commits to origin main...
git push origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ===================================================
    echo   SUCCESS! All changes pushed to GitHub!
    echo ===================================================
) else (
    echo.
    echo ===================================================
    echo   If authentication failed, please ensure you are
    echo   logged into GitHub in your browser or supply a PAT.
    echo ===================================================
)
pause
