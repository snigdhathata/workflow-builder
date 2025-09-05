#!/bin/bash

echo "Starting Workflow Builder..."

echo ""
echo "Starting ChromaDB..."
gnome-terminal -- bash -c "docker run -p 8000:8000 chromadb/chroma; exec bash" 2>/dev/null || \
xterm -e "docker run -p 8000:8000 chromadb/chroma" 2>/dev/null || \
echo "Please start ChromaDB manually: docker run -p 8000:8000 chromadb/chroma"

echo ""
echo "Waiting for ChromaDB to start..."
sleep 5

echo ""
echo "Starting Backend..."
gnome-terminal -- bash -c "cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000; exec bash" 2>/dev/null || \
xterm -e "cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" 2>/dev/null || \
echo "Please start backend manually: cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo ""
echo "Waiting for Backend to start..."
sleep 10

echo ""
echo "Starting Frontend..."
gnome-terminal -- bash -c "cd frontend && npm start; exec bash" 2>/dev/null || \
xterm -e "cd frontend && npm start" 2>/dev/null || \
echo "Please start frontend manually: cd frontend && npm start"

echo ""
echo "========================================"
echo "All services are starting up!"
echo "========================================"
echo ""
echo "ChromaDB: http://localhost:8000"
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Please wait for all services to fully start before using the application."
echo ""
