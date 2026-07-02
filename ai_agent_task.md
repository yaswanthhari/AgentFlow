# AI Integration Task (Beginner Friendly)

Welcome! Your first task is to write a simple Python script that connects to the Google Gemini AI (or another LLM) to get a response for a prompt. This will later be plugged into our main backend.

## Instructions

1.  **Install the library:** Open a terminal in this folder, activate the virtual environment (`.\venv\Scripts\activate`), and install the Google Generative AI package:
    `pip install google-generativeai python-dotenv`

2.  **Get an API Key:** Go to Google AI Studio (aistudio.google.com), sign in, and create a free API key.

3.  **Create an `.env` file:** Create a new file in this folder named exactly `.env` (don't forget the dot). Inside it, add your key like this:
    `GEMINI_API_KEY=your_actual_api_key_here`

4.  **Complete the Script:** I have created a starter file named `ai_agent.py`. Open it and try to write the code that sends the prompt to Gemini and prints the response.

Good luck! If you get stuck, let us know and we can help you debug it.
