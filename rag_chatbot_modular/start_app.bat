@echo off
echo ========================================
echo    RAG Chatbot Startup Script
echo ========================================
echo.

REM Activate conda environment
echo [1/4] Activating conda environment...
call conda activate chatbot
if errorlevel 1 (
    echo ERROR: Failed to activate chatbot environment
    echo Please make sure the environment exists: conda create -n chatbot python=3.9
    pause
    exit /b 1
)

REM Check if Ollama is installed
echo [2/4] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama is not installed or not in PATH
    echo Please install Ollama from: https://ollama.ai/
    pause
    exit /b 1
)

REM Start Ollama server in background
echo [3/4] Starting Ollama server...
start /B ollama serve

REM Wait a moment for Ollama to start
echo Waiting for Ollama server to start...
timeout /t 5 /nobreak >nul

REM Test Ollama connection
echo Testing Ollama connection...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama server may not be ready yet, continuing anyway...
)

REM Start the Flask application
echo [4/4] Starting RAG Chatbot application...
echo.
echo ========================================
echo    Application Starting...
echo ========================================
echo.
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.

python app.py

echo.
echo Application stopped.
pause 