from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse, ChatSessionCreate, ChatSessionResponse
from app.services.chat_service import ChatService
from app.services.workflow_executor import WorkflowExecutor

router = APIRouter()

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session: ChatSessionCreate,
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    service = ChatService(db)
    return await service.create_session(session)

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(
    workflow_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get chat sessions"""
    service = ChatService(db)
    return await service.get_sessions(workflow_id=workflow_id, skip=skip, limit=limit)

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    session_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get messages from a chat session"""
    service = ChatService(db)
    return await service.get_messages(session_id, skip=skip, limit=limit)

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    session_id: int,
    message: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """Send a message and execute the workflow"""
    service = ChatService(db)
    executor = WorkflowExecutor(db)
    
    # Add user message to chat
    user_message = await service.add_message(session_id, message)
    
    # Execute workflow
    try:
        response = await executor.execute_workflow(session_id, message.content)
        
        # Add assistant response to chat
        assistant_message = await service.add_message(
            session_id,
            ChatMessageCreate(
                role="assistant",
                content=response["response"],
                message_metadata=response.get("metadata", {})
            )
        )
        
        return assistant_message
        
    except Exception as e:
        # Add error message to chat
        error_message = await service.add_message(
            session_id,
            ChatMessageCreate(
                role="assistant",
                content=f"Error: {str(e)}",
                message_metadata={"error": True}
            )
        )
        return error_message

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Delete a chat session"""
    service = ChatService(db)
    success = await service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"message": "Chat session deleted successfully"}

