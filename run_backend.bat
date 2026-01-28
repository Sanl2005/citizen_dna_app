cd /d "%~dp0\backend"
echo Starting Backend Server...
call venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
