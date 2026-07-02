# Welcome to AgentFlow

**AgentFlow** is an AI-Powered Agentic Workflow Engine. It allows users to define and execute complex automated tasks powered by AI (Large Language Models) in the background, without freezing or slowing down the main application.

This project is built using modern, "future tech" Python architecture. It demonstrates how to build scalable, enterprise-grade AI software.

---

## 🏗️ The Architecture (How it works)

We have split the project into three distinct layers:

### 1. The Frontend (The Dashboard)
*   **Tech:** HTML, Vanilla JavaScript, and Tailwind CSS.
*   **What it does:** It provides a beautiful, modern UI for users to type in their AI prompts. It uses JavaScript to constantly poll the backend for updates and dynamically changes the status of tasks (from `PENDING` to `PROCESSING` to `COMPLETED`).

### 2. The Backend API (The Brain)
*   **Tech:** Python, FastAPI, SQLAlchemy, and SQLite.
*   **What it does:** This is the lightning-fast web server. When the frontend sends a task, FastAPI immediately saves it to the SQLite database with a status of `PENDING`, pushes it to a background queue, and instantly replies to the frontend. This keeps the web app extremely responsive.

### 3. The Asynchronous Engine (The Muscle)
*   **Tech:** Python, Celery.
*   **What it does:** The Celery worker runs as a completely separate process in the background. It watches the queue for new tasks. When it sees one, it picks it up, changes the database status to `PROCESSING`, and handles the heavy lifting (talking to the AI). Once the AI finishes, Celery saves the result and marks it as `COMPLETED`. 

*(Currently, we bypassed Redis/Docker to make it easier to run locally, so Celery uses the local file system to manage its queue).*

---

## 🚀 How to Run the Project Locally

To run the full stack, you need to open three things:

**1. The Backend API:**
Open a terminal in the `AgentFlow` folder and run:
```powershell
.\venv\Scripts\activate
uvicorn main:app --reload
```
*(The API will run at http://127.0.0.1:8000)*

**2. The Background Worker:**
Open a second terminal in the `AgentFlow` folder and run:
```powershell
.\venv\Scripts\activate
celery -A celery_worker.celery_app worker --loglevel=info --pool=solo
```

**3. The Frontend:**
Simply open the `frontend/index.html` file in any web browser!

---

## 🎯 Current Status & Next Steps

*   **Done:** The database, FastAPI endpoints, Celery asynchronous queue, and the frontend dashboard are all fully built and communicating with each other. 
*   **To Do (The AI Integration):** Right now, the Celery worker just waits 5 seconds and returns fake text to simulate an AI. The next major step is to finish the `ai_agent.py` script to actually connect to the Google Gemini AI API, and then plug that real function into the `celery_worker.py`. 
