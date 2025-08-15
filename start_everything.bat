@echo off
REM Ensure we are in the project root directory
cd /d %~dp0
echo ========================================
echo    Starting Yapper RAG System
echo ========================================
echo.
echo This will start both the backend and frontend servers.
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:3000
echo.
echo Press any key to start...
pause >nul

echo.
echo [1/2] Starting Yapper RAG Backend Server...
echo.
start "Yapper Backend" cmd /k "python yapper_server.py"

echo.
echo [2/2] Waiting for backend to initialize...
echo (This may take a few minutes for the model to load)
echo.

:wait_loop
timeout /t 10 /nobreak >nul
curl -s http://localhost:8001/health >nul 2>&1
if %errorlevel% neq 0 (
    echo Still initializing backend... (waiting)
    goto wait_loop
)

echo.
echo ✅ Backend is ready!
echo.
echo [2/2] Starting Frontend...
echo.
start "Yapper Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo    🎉 Everything is starting up!
echo ========================================
echo.
echo Backend:  http://localhost:8001 (RAG Server)
echo Frontend: http://localhost:3000 (Web Interface)
echo.
echo The frontend will open automatically in a few seconds.
echo If not, manually open: http://localhost:3000
echo.
echo Press any key to open the frontend in your browser...
pause >nul

start http://localhost:3000

echo.
echo Enjoy your Naval RAG assistant! 🚀
echo.
echo To stop everything, close the terminal windows.
pause 