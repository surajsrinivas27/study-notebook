@echo off
REM Quick Start Script for Mini Notebook LLM

echo.
echo ========================================
echo   Mini Notebook LLM - Quick Start
echo ========================================
echo.

REM Check if backend and frontend directories exist
if not exist "backend" (
    echo ERROR: backend directory not found!
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: frontend directory not found!
    pause
    exit /b 1
)

REM Start Backend in a new window
echo.
echo [1/2] Starting Backend (FastAPI)...
echo Please wait for message: "Uvicorn running on http://0.0.0.0:8000"
echo.
start cmd /k "cd backend && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start Frontend in a new window
echo.
echo [2/2] Starting Frontend (React + Vite)...
echo Please wait for message: "Local: http://localhost:5173"
echo.
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Opening frontend in browser...
timeout /t 2 /nobreak

REM Try to open in default browser
start http://localhost:5173

echo.
echo Done! Check your browser.
echo Press Ctrl+C in either terminal to stop servers.
pause
