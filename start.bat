@echo off
echo Starting Workflow Builder...

echo.
echo Starting ChromaDB...
start "ChromaDB" cmd /k "docker run -p 8000:8000 chromadb/chroma"

echo.
echo Waiting for ChromaDB to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Backend...
start "Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Waiting for Backend to start...
timeout /t 10 /nobreak > nul

echo.
echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo All services are starting up!
echo ========================================
echo.
echo ChromaDB: http://localhost:8000
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Please wait for all services to fully start before using the application.
echo.
pause
