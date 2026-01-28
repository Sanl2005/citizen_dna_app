from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, auth
from typing import List

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/message")
def chat_message(
    request: schemas.ChatMessageRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    query = request.message.lower().strip()
    
    # 1. Advanced Normalization & Typo Tolerance
    keyword_map = {
        "educatinal": "education", "educatn": "education", "study": "education", "scholarship": "education", "student": "education",
        "farmer": "kisan", "farming": "kisan", "crop": "kisan", "agriculture": "kisan",
        "woman": "female", "women": "female", "girl": "female", "mothr": "female", "mother": "female", "lady": "female",
        "health": "medical", "hospital": "medical", "illness": "medical", "sick": "medical", "doctor": "medical",
        "money": "income", "cash": "income", "pension": "income", "finance": "income", "old": "senior", "elderly": "senior",
        "house": "awas", "housing": "awas", "home": "awas",
        "startup": "entrepreneur", "business": "entrepreneur", "loan": "entrepreneur",
        "job": "skill", "training": "skill", "work": "skill",
    }

    # Standardize 'abt' and apply keyword corrections
    clean_query = query.replace("abt ", "about ")
    for search_term, target in keyword_map.items():
        if search_term in clean_query:
            clean_query += f" {target}"

    # 2. App-Specific Knowledge Base
    app_knowledge = {
        "digital dna": "Digital DNA is our unique system that creates a socio-economic profile of you based on age, income, and community to match you with government schemes accurately.",
        "welfare stability": "The Welfare Stability Index (Risk Score) is an AI-calculated metric that indicates your level of need for government support. A higher score means you are a high priority for welfare programs.",
        "risk score": "Your Risk Score is calculated using a Random Forest machine learning model trained on over 12,000 citizen records to predict welfare need levels.",
        "apply": "You can check eligibility details for any scheme in the 'Schemes' tab. Once you see a 'Match', click on it to see the specific benefits and requirements.",
        "profile": "Your profile is the heart of the app. By providing accurate details about your education, occupation, and family, our AI can find schemes you didn't even know existed.",
        "who made this": "This app was developed as a state-of-the-art AI governance platform to ensure no citizen is left behind in the digital welfare era.",
    }

    for key, value in app_knowledge.items():
        if key in clean_query:
            return {"reply": f"**DNA Assistant:** {value}"}

    # 3. Scored Scheme Search
    schemes = db.query(models.Scheme).all()
    scored_results = []

    for s in schemes:
        score = 0
        s_name = s.scheme_name.lower()
        s_desc = s.description.lower()
        s_ministry = s.ministry.lower()
        
        # Heavy weight for name matches
        if s_name in clean_query or clean_query in s_name:
            score += 100
        
        # Check against individual query words
        query_words = [w for w in clean_query.split() if len(w) > 2]
        for word in query_words:
            if word in s_name: score += 40
            if word in s_desc: score += 20
            if word in s_ministry: score += 15
            
        # Target audience matching
        if "female" in clean_query and s.required_gender == "Female": score += 50
        if "kisan" in clean_query and "farmer" in s_desc: score += 50
        if "education" in clean_query and ("student" in s_desc or "scholarship" in s_name): score += 50
        
        if score > 0:
            scored_results.append((score, s))

    # Sort results and format response
    scored_results.sort(key=lambda x: x[0], reverse=True)
    top_matches = [item[1] for item in scored_results[:3]]

    if top_matches:
        response = f"I found **{len(top_matches)}** relevant matches based on your interest. Our AI matching engine suggests:\n\n"
        for s in top_matches:
            response += f"🏆 **{s.scheme_name}**\n_{s.ministry}_\n📍 {s.description[:180]}...\n💰 **Benefit:** {s.benefits}\n\n"
        response += "Check your personalized **DNA Match Percentage** for these in the **Schemes tab**."
        return {"reply": response}
    
    # 4. Smart Conversational Fallbacks
    if any(greet in clean_query for greet in ["hello", "hi", "hey", "namaste"]):
        return {"reply": "Namaste! I am your AI Citizen DNA Assistant. I can answer questions about Education, Health, Farming, Women's schemes, or how this app works. How can I guide you?"}
    
    if "how do you work" in clean_query or "how does it work" in clean_query:
        return {"reply": "I use a Random Forest ML model to analyze your 'Digital DNA' (profile) and match it against government eligibility rules. It's fully automated and personalized."}

    # 5. Encouraging Fallback
    return {"reply": "I'm here to help! While I focus on schemes available in our DNA database (like PM-KISAN, Awas Yojana, Health Mission, etc.), I can find more specific gems if you ask about 'Health', 'Farming', or 'Education'. What are you looking for?"}
