from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from bot.config import DATABASE_URL

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    deadline = Column(DateTime, nullable=True)  # Пока не используем, но пригодится

# Создаём движок и таблицы
engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)

# Сессия
Session = sessionmaker(bind=engine)