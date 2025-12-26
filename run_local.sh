#!/bin/bash

# Cleanup existing processes
echo "Cleaning up existing processes on ports 8000 and 3000..."
lsof -ti :8000 | xargs kill -9 2>/dev/null || true
lsof -ti :3000 | xargs kill -9 2>/dev/null || true
rm -f frontend-web/.next/dev/lock || true
sleep 1

# Start Backend
echo "Starting Backend..."
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start Frontend
echo "Starting Frontend..."
cd frontend-web
npm run dev &
FRONTEND_PID=$!

echo "Systems are starting up!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"

# Wait for exit
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
