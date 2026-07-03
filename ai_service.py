import os
from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session
from database import SessionLocal
import models

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def process_ai_task(task_id: int):
    """
    This runs in a FastAPI BackgroundTask.
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
            real_response = "Error: GEMINI_API_KEY is not configured on Render. Please add it to your Environment Variables!"
        else:
            try:
                from google.genai import types
                client = genai.Client(api_key=api_key)
                
                # Persona Logic
                sys_prompt = "You are a helpful AI assistant."
                
                if db_task.persona == "code_sensei":
                    sys_prompt = (
                        "You are Code Sensei, an elite software engineering mentor. "
                        "When given code, explain what it does, reformat it perfectly, "
                        "and add helpful comments. If the user asks a coding question, "
                        "provide a deep, technical explanation with clean code blocks. "
                        "Use markdown, bullet points, and highlight best practices."
                    )
                elif db_task.persona == "resume_roaster":
                    sys_prompt = (
                        "You are the Resume Roaster, a brutally honest but extremely helpful "
                        "Silicon Valley hiring manager. Your job is to critique the user's "
                        "resume or experience. Point out flaws, suggest powerful action verbs, "
                        "and format your feedback with clear markdown headings, bullet points, "
                        "and a 'Final Verdict'. Don't hold back, but be constructive."
                    )
                else:
                    sys_prompt = (
                        "You are an elite, highly advanced AI assistant. Always provide extremely detailed, "
                        "comprehensive, and well-structured answers. Use professional formatting, clear markdown, "
                        "bullet points, bold text for emphasis, and code blocks where applicable."
                    )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=db_task.prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=sys_prompt,
                        temperature=0.7, 
                    )
                )
                real_response = response.text
            except Exception as ai_e:
                real_response = f"AI Error: {str(ai_e)}"
        
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
