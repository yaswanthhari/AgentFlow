# 🚀 AgentFlow: AI-Powered Asynchronous Workflow Engine

AgentFlow is an enterprise-grade, full-stack application demonstrating how to build a scalable, asynchronous background processing engine powered by the latest Large Language Models (Google Gemini 2.5). 

Unlike simple AI chatbots that freeze the UI while waiting for an API response, AgentFlow utilizes a distributed task queue architecture. This ensures the frontend remains lightning-fast and responsive while complex AI tasks are processed in the background.

## 🏗️ Architecture Stack

*   **Frontend:** Vanilla JS, HTML5, and Tailwind CSS v3 (Glassmorphism Dashboard)
*   **Backend API:** FastAPI (Python), SQLite, SQLAlchemy
*   **Task Queue / Background Worker:** Celery
*   **AI Integration:** Google GenAI SDK (Gemini 2.5 Flash)

## 🌟 Key Features

1.  **Asynchronous Processing:** Tasks are instantly saved to the database and pushed to a Celery queue.
2.  **Real-Time Dashboard Polling:** The Javascript frontend continuously polls the API to update UI badges dynamically (`PENDING` ➔ `PROCESSING` ➔ `COMPLETED`).
3.  **Modern Aesthetic:** A sleek, dark-mode UI featuring glassmorphism, animated backgrounds, and responsive design.
4.  **Local Development:** Configured to use a local filesystem broker, avoiding complex Docker/Redis dependencies for easy setup on Windows.

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/AgentFlow.git
   cd AgentFlow
   ```

2. **Set up the Virtual Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure the AI (API Key):**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=AIzaSy...
   ```

## 🚀 Running the Application

You will need to run the web server and the background worker in two separate terminal windows.

**Terminal 1 (FastAPI Server):**
```bash
.\venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 (Celery Worker):**
```bash
.\venv\Scripts\activate
celery -A celery_worker.celery_app worker --loglevel=info --pool=solo
```

**Frontend:**
Simply open `frontend/index.html` in your web browser! No local server is required for the frontend.

## 🤝 Credits
This project was co-created by **Yaswanth Hari** and **Antigravity** (an advanced agentic coding assistant developed by the Google DeepMind team). 

---
*Built as a scalable AI infrastructure prototype.*
