#!/bin/bash
# AdvocaDabra Legal AI System Startup Script
# Starts both backend and frontend servers

echo "Starting AdvocaDabra Legal AI System"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "backend/backend_server.py" ]; then
    echo "Error: backend/backend_server.py not found. Please run from the project root."
    exit 1
fi

# Function to kill processes on exit
cleanup() {
    echo -e "\nShutting down AdvocaDabra..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "  Backend server stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "  Frontend server stopped"
    fi
    echo "AdvocaDabra shutdown complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend server
echo "Starting backend server (Flask)..."
cd backend
python3 backend_server.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Backend server failed to start"
    exit 1
fi

echo "  Backend running on http://localhost:8000"

# Start frontend server
echo "Starting frontend server (Vite)..."
cd frontend/legal-ai-client
npm run dev &
FRONTEND_PID=$!
cd ../..

# Wait a moment for frontend to start
sleep 5

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "Frontend server failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "  Frontend running on http://localhost:5173"
echo ""
echo "AdvocaDabra Legal AI System is ready!"
echo "========================================"
echo "Access the application: http://localhost:5173"
echo "Backend API available: http://localhost:8000/api"
echo "Test the system: python3 test_system.py"
echo ""
echo "Features available:"
echo "   Similar Case Retrieval (SCR)"
echo "   Precedent Case Retrieval (PCR)"
echo "   File Upload & Analysis"
echo "   User Authentication"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "========================================"

# Keep the script running and wait for user interrupt
while true; do
    # Check if processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "Backend server stopped unexpectedly"
        break
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "Frontend server stopped unexpectedly"
        break
    fi
    sleep 5
done

# If we get here, something went wrong
cleanup
