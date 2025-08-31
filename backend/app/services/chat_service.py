from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.chat import ChatSession, ChatMessage
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate

class ChatService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_session(self, session: ChatSessionCreate) -> ChatSession:
        """Create a new chat session"""
        db_session = ChatSession(**session.dict())
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session
    
    async def get_sessions(self, workflow_id: int = None, skip: int = 0, limit: int = 100) -> List[ChatSession]:
        """Get chat sessions"""
        query = self.db.query(ChatSession)
        if workflow_id:
            query = query.filter(ChatSession.workflow_id == workflow_id)
        return query.offset(skip).limit(limit).all()
    
    async def get_session(self, session_id: int) -> Optional[ChatSession]:
        """Get a specific chat session"""
        return self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    async def delete_session(self, session_id: int) -> bool:
        """Delete a chat session"""
        db_session = await self.get_session(session_id)
        if not db_session:
            return False
        
        self.db.delete(db_session)
        self.db.commit()
        return True
    
    async def add_message(self, session_id: int, message: ChatMessageCreate) -> ChatMessage:
        """Add a message to a chat session"""
        db_message = ChatMessage(**message.dict(), session_id=session_id)
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
    
    async def get_messages(self, session_id: int, skip: int = 0, limit: int = 100) -> List[ChatMessage]:
        """Get messages from a chat session"""
        return self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).offset(skip).limit(limit).all()


