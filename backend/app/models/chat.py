from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    session_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON, nullable=True)  # Additional data like sources, execution time, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    session = relationship("ChatSession", back_populates="messages")

