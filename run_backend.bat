@echo off
cd /d "%~dp0"
echo Starting Backend Server...
call backend\venv\Scripts\activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
