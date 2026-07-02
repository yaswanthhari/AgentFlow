import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("NO API KEY FOUND")
else:
    client = genai.Client(api_key=api_key)
    print("AVAILABLE MODELS:")
    for m in client.models.list():
        print(m.name)
