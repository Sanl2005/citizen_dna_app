def get_chat_response(message: str) -> str:
    """
    Intelligent chatbot for Citizen Digital DNA - provides helpful responses about Indian government schemes.
    No API key required - works 100% offline.
    """
    message_lower = message.lower()
    
    # Scheme-specific responses
    if any(word in message_lower for word in ["pm kisan", "pmkisan", "kisan"]):
        return ("PM-KISAN provides ₹6,000/year to farmer families in 3 installments. "
                "Eligibility: Small & marginal farmers with cultivable land. "
                "Apply online at: pmkisan.gov.in with your Aadhaar.")
    
    elif any(word in message_lower for word in ["ayushman", "health", "hospital", "medical"]):
        return ("Ayushman Bharat provides ₹5 lakh health cover for hospitalization. "
                "Eligibility: Families identified through SECC-2011 data. "
                "Check eligibility & get card at: pmjay.gov.in")
    
    elif any(word in message_lower for word in ["housing", "awas", "house", "home"]):
        return ("PM Awas Yojana provides subsidy for constructing/buying houses. "
                "Eligibility: EWS/LIG families without pucca house. "
                "Apply through: pmaymis.gov.in with income & property documents.")
    
    elif any(word in message_lower for word in ["pension", "old age", "senior citizen"]):
        return ("National Social Assistance Programme provides ₹200-500/month pension for elderly (60+), widows, and persons with disabilities. "
                "Apply at: District Social Welfare Office with age proof.")
    
    elif any(word in message_lower for word in ["scholarship", "student", "education"]):
        return ("Multiple scholarship schemes available: NSP, Post-Matric, Merit-cum-Means. "
                "Check eligibility at: scholarships.gov.in based on category, income, and marks.")
    
    elif any(word in message_lower for word in ["ration", "food", "pds"]):
        return ("Public Distribution System provides subsidized food grains. "
                "Eligibility: AAY/PHH/Priority households with ration card. "
                "Apply at: Tehsil/Block office with income certificate.")
    
    elif any(word in message_lower for word in ["mudra", "loan", "business"]):
        return ("PM MUDRA Yojana provides loans up to ₹10 lakh for small businesses. "
                "Categories: Shishu (₹50k), Kishore (₹5L), Tarun (₹10L). "
                "Apply at: Any bank/NBFC with business plan.")
    
    elif any(word in message_lower for word in ["eligibility", "eligible", "qualify"]):
        return ("Eligibility varies by scheme. Common criteria: Income limits, age, landholding, caste category. "
                "Tell me which specific scheme you're interested in, and I'll explain the eligibility!")
    
    elif any(word in message_lower for word in ["apply", "application", "how to"]):
        return ("Most schemes require: Aadhaar, Bank account, Income certificate, Caste certificate (if applicable). "
                "Applications can be submitted online through official portals or at local government offices.")
    
    elif any(word in message_lower for word in ["help", "hi", "hello", "namaste"]):
        return ("Namaste! I'm your Citizen DNA Assistant. I can help you with information about: "
                "PM Kisan, Ayushman Bharat, PM Awas, Scholarships, Pensions, and more. What would you like to know?")
    
    else:
        return ("I can help you learn about Indian government welfare schemes like PM-KISAN, Ayushman Bharat, PM Awas Yojana, scholarships, pensions, and more. "
                "What specific scheme or benefit are you looking for information about?")
