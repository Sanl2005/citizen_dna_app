import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Define the system prompt / context
PROJECT_SCOPE = """
You are the AI Assistant for the 'Citizen Digital DNA' application.
Your goal is to help Indian citizens discover and understand government schemes and benefits they are eligible for.

Project Scope & Capabilities:
1. Provide accurate information about Indian Government Schemes (PM-KISAN, Ayushman Bharat, etc.).
2. Explain eligibility criteria, application processes, and required documents.
3. Simplify complex bureaucratic language into easy-to-understand explanations.
4. Assist users in checking their potential eligibility based on details they provide (age, income, occupation, etc.).
5. Be polite, helpful, and empathetic. See yourself as a digital social worker.

Limitations:
- Do not provide medical, legal, or financial advice beyond general scheme information.
- If unsure about a specific recent update, advise the user to check the official government portal.
- Stay strictly within the domain of Indian Government Welfare Schemes and the Citizen Digital DNA app.
- If asked about topics outside this scope (e.g., coding, movies, general trivia), politely redirect the conversation back to government schemes or decline to answer.

Key Schemes to know (but not limited to):
- PM-KISAN (Agriculture)
- Ayushman Bharat (Health)
- PM Awas Yojana (Housing)
- National Social Assistance Programme (Pensions)
- Scholarships (Education)
- PDS / Ration Card (Food Security)
- PM Mudra Yojana (Loans)
"""

async def get_chat_response(message: str) -> str:
    """
    Generates a response using Google's Gemini model, grounded in the project scope.
    """
    if not GEMINI_API_KEY:
        return "Error: Gemini API Key is missing. Please configure GEMINI_API_KEY in .env file."

    try:
        # List of models to try in order of preference
        candidate_models = ['models/gemini-flash-latest', 'models/gemini-pro-latest']
        
        model = None
        last_error = None

        # 1. Try to initialize with a specific model
        for model_name in candidate_models:
            try:
                # We don't make an API call yet, just setup
                model = genai.GenerativeModel(model_name)
                # Test connectivity with a dry run or simple prompt
                # But creating the object usually doesn't validate. 
                # We will just proceed to use the first one and catch the specific generation error.
                break 
            except Exception:
                continue

        if not model:
             model = genai.GenerativeModel('gemini-pro')

        # Creating a prompt with context
        full_prompt = f"{PROJECT_SCOPE}\n\nUser Query: {message}\n\nAssistant Response:"
        
        # Async generation
        # We wrap this in a try/except specifically for the generation call
        try:
           response = await model.generate_content_async(full_prompt)
        except Exception as e:
            # Return the error directly so we can debug the primary model failure
            print(f"Primary model failed: {e}")
            return f"Error with model {candidate_models[0]}: {str(e)}"

        if response.text:
            return response.text
        else:
            return "I apologize, but I couldn't generate a response at this moment."
            
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"I'm currently unable to connect to the AI service. Error: {str(e)}"
