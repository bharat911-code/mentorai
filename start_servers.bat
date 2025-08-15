@echo off
echo Starting Naval Ravikant AI Chat (Full ML Version)...
echo.

echo Installing full Python dependencies...
pip install --user -r requirements.txt

echo.
echo Starting Full FastAPI Backend with ML...
start "FastAPI Backend" cmd /k "cd /d %~dp0 && python -m uvicorn api_server:app --reload --port 8000"

echo Starting Vite Frontend...
start "Vite Frontend" cmd /k "cd /d %~dp0 && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Note: The ML model will take time to download and initialize on first run.
echo Wait for "Model and index initialized successfully!" before testing.
echo.
echo Press any key to close this window...
pause >nul 