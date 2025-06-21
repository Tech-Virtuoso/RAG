Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    RAG Chatbot Startup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate conda environment
Write-Host "[1/4] Activating conda environment..." -ForegroundColor Yellow
try {
    conda activate chatbot
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to activate environment"
    }
} catch {
    Write-Host "ERROR: Failed to activate chatbot environment" -ForegroundColor Red
    Write-Host "Please make sure the environment exists: conda create -n chatbot python=3.9" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Ollama is installed
Write-Host "[2/4] Checking Ollama installation..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Ollama not found"
    }
    Write-Host "Ollama version: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Ollama is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Ollama from: https://ollama.ai/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Start Ollama server in background
Write-Host "[3/4] Starting Ollama server..." -ForegroundColor Yellow
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden

# Wait for Ollama to start
Write-Host "Waiting for Ollama server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test Ollama connection
Write-Host "Testing Ollama connection..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 10
    Write-Host "✓ Ollama server is running" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Ollama server may not be ready yet, continuing anyway..." -ForegroundColor Yellow
}

# Start the Flask application
Write-Host "[4/4] Starting RAG Chatbot application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Application Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The application will be available at: http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

python app.py

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit" 