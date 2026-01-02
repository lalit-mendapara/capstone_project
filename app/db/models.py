# Defines how the chat history is saved in the relational database.

from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
from datetime import datetime,timezone

class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))