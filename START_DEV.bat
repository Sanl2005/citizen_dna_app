@echo off
TITLE Citizen Digital DNA - System Launcher
echo ==========================================
echo    CITIZEN DIGITAL DNA - SYSTEM LAUNCHER
echo ==========================================
echo.

:: Detect if we are in the right directory
if not exist "backend" (
    echo [ERROR] Directory 'backend' not found. Please run this from the project root.
    pause
    exit /b
)

echo [STEP 1/2] Starting Backend Server (FastAPI)...
start "Backend Server" cmd /k "cd backend && call venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo [STEP 2/2] Starting Frontend App (Expo)...
start "Frontend Web" cmd /k "cd citizen_dna_app && npx expo start"

echo.
echo ==========================================
echo SUCCESS: Both servers are starting!
echo.
echo Local API: http://localhost:8000
echo Network API: http://10.57.204.242:8000
echo.
echo Frontend: http://localhost:8081
echo ==========================================
echo.
echo Press any key to exit this launcher (servers will remain running)...
pause > nul
