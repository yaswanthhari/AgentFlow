import os
import time
from dotenv import load_dotenv
from google import genai
from celery import Celery
from sqlalchemy.orm import Session
from database import SessionLocal
import models

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
# Configuration is handled per client instance in the new SDK.

# Check if we are in production (Render) by looking for the Redis URL
redis_url = os.getenv("CELERY_BROKER_URL")

if redis_url:
    # Production: Use Redis
    celery_app = Celery("agentflow_worker", broker=redis_url, backend="sqlite:///celery_results.db")
else:
    # Local: Use file system
    os.makedirs('./broker/out', exist_ok=True)
    os.makedirs('./broker/processed', exist_ok=True)
    
    celery_app = Celery("agentflow_worker", broker="filesystem://localhost//", backend="sqlite:///celery_results.db")
    celery_app.conf.update(
        broker_transport_options={
            'data_folder_in': './broker/out',
            'data_folder_out': './broker/out',
            'data_folder_processed': './broker/processed'
        }
    )

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(name="process_ai_task")
def process_ai_task(task_id: int):
    """
    This is the background task that will run independently of the web API.
    It simulates picking up a task, calling the AI, and saving the result.
    """
    db: Session = SessionLocal()
    try:
        # Fetch the task from the database
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not db_task:
            return f"Task {task_id} not found"

        # Update status to processing
        db_task.status = "PROCESSING"
        db.commit()

        print(f"[{task_id}] Sending prompt to Gemini: '{db_task.prompt}'...")
        
        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            real_response = "Error: GEMINI_API_KEY is not configured in the .env file. Please add it to start using real AI!"
        else:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=db_task.prompt
            )
            real_response = response.text
        
        # Save the result
        db_task.result = real_response
        db_task.status = "COMPLETED"
        db.commit()
        
        return real_response

    except Exception as e:
        db.rollback()
        if db_task:
            db_task.status = "FAILED"
            db_task.result = str(e)
            db.commit()
        raise e
    finally:
        db.close()
