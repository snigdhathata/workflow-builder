#!/bin/bash

echo "Setting up Workflow Builder Project..."

echo ""
echo "========================================"
echo "1. Setting up Backend"
echo "========================================"
cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Creating .env file..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "Please edit .env file with your API keys and database configuration"
fi

echo ""
echo "========================================"
echo "2. Setting up Frontend"
echo "========================================"
cd ../frontend

echo "Installing Node.js dependencies..."
npm install

echo "Creating .env file..."
if [ ! -f .env ]; then
    echo "REACT_APP_API_URL=http://localhost:8000" > .env
fi

echo ""
echo "========================================"
echo "3. Database Setup Instructions"
echo "========================================"
echo ""
echo "Please follow these steps to set up your database:"
echo ""
echo "1. Install PostgreSQL and create a database:"
echo "   createdb workflow_db"
echo ""
echo "2. Update the DATABASE_URL in backend/.env file"
echo ""
echo "3. Run database migrations:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   alembic upgrade head"
echo ""
echo "4. Start ChromaDB (for vector storage):"
echo "   docker run -p 8000:8000 chromadb/chroma"
echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. Start the frontend (in a new terminal):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
