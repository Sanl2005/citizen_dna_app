import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

async def find_model():
    candidates = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro",
        "models/gemini-1.5-flash",
        "gemini-2.0-flash-exp",
    ]
    
    print(f"Testing with API Key: {api_key[:5]}...")
    
    for name in candidates:
        print(f"\nTesting model: {name}")
        try:
            model = genai.GenerativeModel(name)
            response = await model.generate_content_async("Test")
            print(f"SUCCESS! Model '{name}' works. Response: {response.text}")
            return
        except Exception as e:
            print(f"FAILED '{name}': {e}")

if __name__ == "__main__":
    asyncio.run(find_model())
