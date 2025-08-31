from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import workflows, documents, chat
from app.core.config import settings

app = FastAPI(
    title="Workflow Builder API",
    description="No-Code/Low-Code Workflow Builder Backend API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["workflows"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Workflow Builder API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

