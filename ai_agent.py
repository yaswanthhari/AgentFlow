import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Configure the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY is not set in the .env file.")
    exit(1)

genai.configure(api_key=api_key)

def ask_ai(prompt: str):
    """
    This function should take a prompt, send it to the Gemini model, 
    and return the text response.
    """
    # TODO: Initialize the model (e.g., 'gemini-1.5-flash')
    # TODO: Send the prompt to the model and get the response
    # TODO: Return the response text
    
    pass

if __name__ == "__main__":
    # Test your function here
    test_prompt = "Explain quantum computing in one simple sentence."
    print("Sending prompt:", test_prompt)
    
    response = ask_ai(test_prompt)
    
    print("\nAI Response:")
    print(response)
