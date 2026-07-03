from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db
from ai_service import process_ai_task
from fastapi.staticfiles import StaticFiles
import os

# Create all database tables
models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AgentFlow API", description="AI-Powered Agentic Workflow Engine")

# Mount the frontend directory to serve static files
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/dashboard", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schemas for Requests ---
class UserCreate(BaseModel):
    email: str

class WorkflowCreate(BaseModel):
    title: str
    description: str
    owner_id: int

class TaskCreate(BaseModel):
    prompt: str
    persona: str = "general"
    workflow_id: int

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to AgentFlow API"}

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/workflows/")
def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    db_workflow = models.Workflow(
        title=workflow.title, 
        description=workflow.description, 
        owner_id=workflow.owner_id
    )
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@app.post("/tasks/")
def create_task(task: TaskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Save the initial task to the database with PENDING status
    db_task = models.Task(prompt=task.prompt, persona=task.persona, workflow_id=task.workflow_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # 2. Trigger the native FastAPI background task
    background_tasks.add_task(process_ai_task, db_task.id)
    
    return {"message": "Task queued successfully", "task_id": db_task.id, "status": "PENDING"}

@app.get("/tasks/")
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.id.desc()).all()
    return [{"task_id": t.id, "prompt": t.prompt, "persona": t.persona, "status": t.status, "result": t.result} for t in tasks]

@app.get("/tasks/{task_id}")
def get_task_status(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task.id, "prompt": task.prompt, "persona": task.persona, "status": task.status, "result": task.result}
