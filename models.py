from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    workflows = relationship("Workflow", back_populates="owner")

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="workflows")
    tasks = relationship("Task", back_populates="workflow")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String)
    persona = Column(String, default="general") # Which AI persona to use
    status = Column(String, default="PENDING") # PENDING, PROCESSING, COMPLETED, FAILED
    result = Column(String, nullable=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    
    workflow = relationship("Workflow", back_populates="tasks")
