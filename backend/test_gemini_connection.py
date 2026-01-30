import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key present: {bool(api_key)}")
if api_key:
    # Print first few chars to verify it's the right one (safe to log locally)
    print(f"API Key start: {api_key[:5]}...")

genai.configure(api_key=api_key)

async def test_chat():
    try:
        print("Attempting to create model 'gemini-1.5-flash'...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("Generating content...")
        response = await model.generate_content_async("Hello, can you hear me?")
        
        print("Response received:")
        if response.text:
            print(response.text)
        else:
            print("Response object exists but no text.")
            
    except Exception as e:
        print("\nCRITICAL ERROR DETECTED:")
        print(f"Type: {type(e)}")
        print(f"Message: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chat())
