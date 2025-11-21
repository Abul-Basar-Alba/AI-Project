#!/bin/bash

# HealthNest AI - Quick Start Script
# Runs the complete application (backend + frontend)

echo "=================================================="
echo "🚀 Starting HealthNest AI Application"
echo "=================================================="
echo ""

# Check if models exist
if [ ! -f "models/qa_vectorizer.pkl" ]; then
    echo "⚠️  Models not found. Running setup first..."
    bash setup.sh
    echo ""
fi

# Start backend in background
echo "🔄 Starting backend server..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""

# Wait for backend to be ready
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
curl -s http://localhost:5000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend is ready!"
else
    echo "⚠️  Backend might not be ready yet. Please wait..."
fi

echo ""
echo "=================================================="
echo "✅ HealthNest AI is Running!"
echo "=================================================="
echo ""
echo "🌐 Backend API: http://localhost:5000"
echo "📱 Frontend: Open frontend/index.html in your browser"
echo ""
echo "Or start a frontend server:"
echo "  cd frontend"
echo "  python3 -m http.server 8000"
echo "  Visit: http://localhost:8000"
echo ""
echo "📝 To stop the application, press Ctrl+C"
echo "=================================================="
echo ""

# Keep script running
wait $BACKEND_PID
