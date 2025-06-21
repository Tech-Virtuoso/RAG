@echo off
echo ========================================
echo    Ollama Windows Service Setup
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ Running as administrator
) else (
    echo ERROR: This script must be run as administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Check if Ollama is installed
echo [1/4] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama is not installed or not in PATH
    echo Please install Ollama from: https://ollama.ai/
    pause
    exit /b 1
)

REM Get Ollama path
for /f "tokens=*" %%i in ('where ollama') do set OLLAMA_PATH=%%i
echo Found Ollama at: %OLLAMA_PATH%

REM Create service using sc command
echo [2/4] Creating Ollama Windows service...
sc create "Ollama" binPath= "%OLLAMA_PATH% serve" start= auto DisplayName= "Ollama AI Server"
if errorlevel 1 (
    echo ERROR: Failed to create service
    pause
    exit /b 1
)

REM Set service description
echo [3/4] Setting service description...
sc description "Ollama" "Ollama AI Server - Provides local LLM and embedding services"
if errorlevel 1 (
    echo WARNING: Failed to set description, but service was created
)

REM Start the service
echo [4/4] Starting Ollama service...
sc start "Ollama"
if errorlevel 1 (
    echo WARNING: Failed to start service automatically
    echo You may need to start it manually from Services
) else (
    echo ✓ Ollama service started successfully
)

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Ollama will now start automatically when Windows boots
echo.
echo To manage the service:
echo - Start:   sc start Ollama
echo - Stop:    sc stop Ollama
echo - Status:  sc query Ollama
echo - Remove:  sc delete Ollama
echo.
echo You can also manage it from Windows Services (services.msc)
echo.
pause 