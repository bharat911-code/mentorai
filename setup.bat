@echo off
echo Setting up Naval Ravikant AI Chat...
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Installing Node.js dependencies...
npm install

echo.
echo Setup complete!
echo.
echo To run the application:
echo 1. Double-click start_servers.bat
echo 2. Or run manually:
echo    - Backend: uvicorn api_server:app --reload --port 8000
echo    - Frontend: npm run dev
echo.
echo Optional: Set your HuggingFace token for better model access:
echo set HFT_TOKEN=your_token_here
echo.
pause 