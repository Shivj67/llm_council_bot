from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # Telegram User ID
    mode = Column(String(50), default='learning')
    council_depth = Column(String(20), default='standard') # quick, standard, deep
    persona = Column(String(50), default='balanced')

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    role = Column(String(20)) # user, assistant
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    query = Column(Text)
    agent_name = Column(String(50))
    agent_output = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database Setup
engine = create_engine('sqlite:///council.db')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_session():
    return Session()
