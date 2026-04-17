#!/bin/bash

# Quick Start Script for Mini Notebook LLM (Mac/Linux)

echo ""
echo "========================================"
echo "  Mini Notebook LLM - Quick Start"
echo "========================================"
echo ""

# Check if backend and frontend directories exist
if [ ! -d "backend" ]; then
    echo "ERROR: backend directory not found!"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "ERROR: frontend directory not found!"
    exit 1
fi

# Start Backend in background
echo ""
echo "[1/2] Starting Backend (FastAPI)..."
echo "Please wait for message: 'Uvicorn running on http://0.0.0.0:8000'"
echo ""
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start Frontend in background
echo ""
echo "[2/2] Starting Frontend (React + Vite)..."
echo "Please wait for message: 'Local: http://localhost:5173'"
echo ""
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Opening frontend in browser..."
sleep 2

# Try to open in default browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
elif command -v open &> /dev/null; then
    open http://localhost:5173
else
    echo "Please open http://localhost:5173 in your browser"
fi

echo ""
echo "Done! Both servers are running."
echo "Press Ctrl+C to stop all servers."
echo ""

# Wait for user to stop
wait $BACKEND_PID $FRONTEND_PID
