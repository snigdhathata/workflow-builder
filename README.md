<<<<<<< HEAD
# workflow-builder
=======
# No-Code/Low-Code Workflow Builder

A full-stack web application that enables users to visually create and interact with intelligent workflows using drag-and-drop components.

## Features

- **Visual Workflow Builder**: Drag-and-drop interface using React Flow
- **Four Core Components**:
  - User Query Component (entry point)
  - KnowledgeBase Component (document processing & embeddings)
  - LLM Engine Component (AI processing)
  - Output Component (chat interface)
- **Document Processing**: PDF text extraction and embedding generation
- **AI Integration**: OpenAI GPT and Gemini support
- **Web Search**: SerpAPI integration
- **Vector Database**: ChromaDB for semantic search
- **Real-time Chat**: Interactive query processing

## Tech Stack

- **Frontend**: React.js with TypeScript
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Drag & Drop**: React Flow
- **Vector Store**: ChromaDB
- **Embeddings**: OpenAI Embeddings, Gemini
- **LLM**: OpenAI GPT, Gemini
- **Web Search**: SerpAPI
- **Text Extraction**: PyMuPDF

## Project Structure

```
project/
├── frontend/                 # React.js frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   └── types/          # TypeScript types
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
├── database/               # Database migrations
└── docs/                   # Documentation
```

## Quick Start

### Prerequisites

- Node.js (v18+)
- Python (v3.9+)
- PostgreSQL
- Docker (optional)

### Environment Variables

Create `.env` files in both frontend and backend directories:

**Backend (.env):**
```
DATABASE_URL=postgresql://user:password@localhost:5432/workflow_db
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
SERPAPI_API_KEY=your_serpapi_key
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

**Frontend (.env):**
```
REACT_APP_API_URL=http://localhost:8000
```

### Installation

1. **Clone and setup backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Setup database:**
```bash
# Start PostgreSQL and create database
createdb workflow_db
# Run migrations
alembic upgrade head
```

3. **Start backend:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Setup frontend:**
```bash
cd frontend
npm install
```

5. **Start frontend:**
```bash
npm start
```

6. **Start ChromaDB:**
```bash
docker run -p 8000:8000 chromadb/chroma
```

## Usage

1. Open the application in your browser (http://localhost:3000)
2. Drag components from the left panel to the workspace
3. Connect components to create a workflow
4. Configure each component with required parameters
5. Click "Build Stack" to validate the workflow
6. Click "Chat with Stack" to start interacting with your workflow

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

The application follows a modular architecture:

1. **Frontend**: React-based UI with React Flow for workflow visualization
2. **Backend**: FastAPI with modular services for each component type
3. **Database**: PostgreSQL for metadata and ChromaDB for vector storage
4. **External APIs**: OpenAI, Gemini, SerpAPI for AI and search capabilities

## Development

### Adding New Components

1. Create component in `frontend/src/components/`
2. Add to component library in `frontend/src/components/ComponentLibrary.tsx`
3. Create corresponding backend service in `backend/app/services/`
4. Add API endpoints in `backend/app/api/`

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```


>>>>>>> bab65138 (Initial commit)
