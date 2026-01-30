import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

with open("available_models.txt", "w") as f:
    try:
        f.write("--- START MODEL LIST ---\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"NAME: {m.name}\n")
        f.write("--- END MODEL LIST ---\n")
    except Exception as e:
        f.write(f"ERROR: {e}\n")
