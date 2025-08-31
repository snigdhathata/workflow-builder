# Project Structure

This document provides a detailed overview of the No-Code/Low-Code Workflow Builder project structure.

## Root Directory

```
project/
├── README.md                 # Main project documentation
├── PROJECT_STRUCTURE.md      # This file - detailed structure
├── setup.sh                  # Unix/Linux setup script
├── setup.bat                 # Windows setup script
├── backend/                  # FastAPI backend application
├── frontend/                 # React.js frontend application
└── docs/                     # Additional documentation
```

## Backend Structure

```
backend/
├── requirements.txt          # Python dependencies
├── env.example              # Environment variables template
├── alembic.ini              # Database migration configuration
├── alembic/                 # Database migrations
│   └── env.py               # Alembic environment setup
├── uploads/                 # File upload directory
└── app/                     # Main application package
    ├── __init__.py
    ├── main.py              # FastAPI application entry point
    ├── core/                # Core configuration
    │   ├── __init__.py
    │   ├── config.py        # Settings and environment variables
    │   └── database.py      # Database connection and session
    ├── models/              # SQLAlchemy database models
    │   ├── __init__.py
    │   ├── workflow.py      # Workflow and component models
    │   ├── document.py      # Document model
    │   └── chat.py          # Chat session and message models
    ├── schemas/             # Pydantic data validation schemas
    │   ├── __init__.py
    │   ├── workflow.py      # Workflow data schemas
    │   ├── document.py      # Document data schemas
    │   └── chat.py          # Chat data schemas
    ├── api/                 # FastAPI route handlers
    │   ├── __init__.py
    │   ├── workflows.py     # Workflow CRUD operations
    │   ├── documents.py     # Document upload and management
    │   └── chat.py          # Chat and workflow execution
    ├── services/            # Business logic services
    │   ├── __init__.py
    │   ├── workflow_service.py      # Workflow management
    │   ├── document_service.py      # Document processing
    │   ├── chat_service.py          # Chat management
    │   └── workflow_executor.py     # Workflow execution engine
    └── utils/               # Utility functions and services
        ├── __init__.py
        ├── text_extractor.py        # PDF text extraction
        ├── embedding_service.py     # Vector embeddings
        ├── llm_service.py           # AI model integration
        └── web_search_service.py    # Web search integration
```

## Frontend Structure

```
frontend/
├── package.json             # Node.js dependencies and scripts
├── env.example              # Environment variables template
├── tailwind.config.js       # Tailwind CSS configuration
├── postcss.config.js        # PostCSS configuration
├── public/                  # Static assets
│   ├── index.html           # Main HTML template
│   ├── favicon.ico          # Application icon
│   └── manifest.json        # PWA manifest
└── src/                     # React application source
    ├── index.tsx            # React entry point
    ├── index.css            # Global styles with Tailwind
    ├── App.tsx              # Main application component
    ├── types/               # TypeScript type definitions
    │   └── index.ts         # All type definitions
    ├── services/            # API service layer
    │   └── api.ts           # Backend API integration
    ├── components/          # Reusable React components
    │   ├── Navbar.tsx       # Navigation component
    │   ├── ComponentLibrary.tsx     # Component library panel
    │   ├── ComponentConfigPanel.tsx # Component configuration
    │   └── WorkflowToolbar.tsx      # Workflow action toolbar
    └── pages/               # Page components
        ├── WorkflowBuilder.tsx      # Main workflow builder
        └── ChatInterface.tsx        # Chat interaction interface
```

## Key Features by Component

### Backend Components

#### Core Components
- **Configuration Management**: Environment variables, database settings
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **API Framework**: FastAPI with automatic documentation

#### Models
- **Workflow**: Workflow definitions and metadata
- **WorkflowComponent**: Individual components with configuration
- **Document**: File upload and processing metadata
- **Chat**: Session and message management

#### Services
- **WorkflowService**: CRUD operations for workflows
- **DocumentService**: File upload and processing
- **ChatService**: Chat session management
- **WorkflowExecutor**: Workflow execution engine

#### Utilities
- **TextExtractor**: PDF text extraction using PyMuPDF
- **EmbeddingService**: Vector embeddings with OpenAI/Gemini
- **LLMService**: AI model integration (OpenAI, Gemini)
- **WebSearchService**: Web search with SerpAPI

### Frontend Components

#### Core Features
- **React Flow Integration**: Drag-and-drop workflow builder
- **Component Library**: Pre-built workflow components
- **Configuration Panel**: Component settings interface
- **Chat Interface**: Real-time workflow interaction

#### Components
- **ComponentLibrary**: Draggable component palette
- **ComponentConfigPanel**: Dynamic configuration forms
- **WorkflowToolbar**: Action buttons and controls
- **ChatInterface**: Interactive chat with workflows

## Data Flow

1. **Workflow Creation**: User drags components to canvas
2. **Configuration**: Components are configured via right panel
3. **Validation**: Workflow is validated for correctness
4. **Execution**: User queries are processed through workflow
5. **Response**: AI-generated responses are returned via chat

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy
- **AI/ML**: OpenAI GPT, Google Gemini
- **Vector Store**: ChromaDB
- **File Processing**: PyMuPDF
- **Web Search**: SerpAPI

### Frontend
- **Framework**: React.js with TypeScript
- **UI Library**: Tailwind CSS
- **Flow Builder**: React Flow
- **HTTP Client**: Axios
- **Icons**: Lucide React

### Infrastructure
- **Database**: PostgreSQL
- **Vector Database**: ChromaDB (Docker)
- **File Storage**: Local filesystem
- **Development**: Hot reload for both frontend and backend

## API Endpoints

### Workflows
- `GET /api/v1/workflows/` - List workflows
- `POST /api/v1/workflows/` - Create workflow
- `GET /api/v1/workflows/{id}` - Get workflow
- `PUT /api/v1/workflows/{id}` - Update workflow
- `DELETE /api/v1/workflows/{id}` - Delete workflow
- `POST /api/v1/workflows/{id}/validate` - Validate workflow

### Documents
- `GET /api/v1/documents/` - List documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/{id}` - Get document
- `DELETE /api/v1/documents/{id}` - Delete document
- `POST /api/v1/documents/{id}/process` - Process document

### Chat
- `GET /api/v1/chat/sessions` - List chat sessions
- `POST /api/v1/chat/sessions` - Create session
- `GET /api/v1/chat/sessions/{id}/messages` - Get messages
- `POST /api/v1/chat/sessions/{id}/messages` - Send message
- `DELETE /api/v1/chat/sessions/{id}` - Delete session

## Development Workflow

1. **Setup**: Run setup script to install dependencies
2. **Configuration**: Update environment variables
3. **Database**: Start PostgreSQL and run migrations
4. **Services**: Start ChromaDB and backend
5. **Frontend**: Start React development server
6. **Testing**: Use API documentation at `/docs`

## Deployment Considerations

- **Environment Variables**: Secure API keys and database credentials
- **Database**: Use managed PostgreSQL service
- **File Storage**: Consider cloud storage for production
- **Vector Database**: Deploy ChromaDB with persistence
- **Frontend**: Build and serve static files
- **Backend**: Deploy with ASGI server (Gunicorn + Uvicorn)


