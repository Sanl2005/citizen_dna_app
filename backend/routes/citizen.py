from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database, models, schemas, auth
# Will import AI service later

router = APIRouter(
    prefix="/citizen",
    tags=["Citizen"]
)

@router.post("/profile", response_model=schemas.ProfileResponse)
def create_or_update_profile(
    profile: schemas.ProfileCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    # Check if profile exists
    db_profile = db.query(models.CitizenProfile).filter(models.CitizenProfile.user_id == current_user.id).first()
    
    if db_profile:
        # Update existing
        for key, value in profile.dict().items():
            setattr(db_profile, key, value)
    else:
        # Create new
        db_profile = models.CitizenProfile(**profile.dict(), user_id=current_user.id)
        db.add(db_profile)
    
    # Calculate Risk Score using AI Engine
    from services.ai_engine import ai_engine
    
    # Prepare data for AI
    ai_input = {
        "age": db_profile.age,
        "income": db_profile.income,
        "family_size": db_profile.family_size,
        "disability_status": db_profile.disability_status,
        "education": db_profile.education,
        "occupation": db_profile.occupation,
        "location": db_profile.location_state,
        "location_type": db_profile.location_type,
        "community": db_profile.community,
        "gender": db_profile.gender
    }
    
    score = ai_engine.predict_risk(ai_input)
    db_profile.risk_score_health = score
    db_profile.risk_score_financial = score # Simplification for demo, could train 2 models

    
    # Generate Real-time Recommendations
    # 1. Clear old recommendations
    db.query(models.Recommendation).filter(models.Recommendation.user_id == current_user.id).delete()
    
    # 2. Match with available schemes
    all_schemes = db.query(models.Scheme).all()
    for s in all_schemes:
        match = False
        reasons = []
        
        # Simple Logic Engine
        if s.min_age and db_profile.age >= s.min_age:
            match = True
            reasons.append(f"Eligible for age {db_profile.age}")
            
        if s.max_income and db_profile.income <= s.max_income:
            match = True
            reasons.append(f"Income ₹{db_profile.income} is within limits")
            
        if s.required_gender and db_profile.gender == s.required_gender:
            match = True
            reasons.append(f"Dedicated benefit for {db_profile.gender}")
            
        if "Rural" in s.description and db_profile.location_type == "Rural":
            match = True
            reasons.append("Rural area support")

        if db_profile.community and (db_profile.community in s.scheme_name or db_profile.community in s.description):
            match = True
            reasons.append(f"Targeted for {db_profile.community} category")

        if score > 0.6: # High risk = high priority for welfare
            match = True
            reasons.append("High priority welfare match")

        if match:
            # Boost confidence for community/gender matches
            confidence = 0.8 + (score * 0.1)
            if db_profile.community and db_profile.community in s.scheme_name:
                confidence += 0.1
            
            new_rec = models.Recommendation(
                user_id=current_user.id,
                scheme_id=s.id,
                confidence_score=min(confidence, 0.99),
                reason=" and ".join(reasons[:2]) or "AI predicted match based on DNA profile"
            )
            db.add(new_rec)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/profile", response_model=schemas.ProfileResponse)
def get_profile(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    db_profile = db.query(models.CitizenProfile).filter(models.CitizenProfile.user_id == current_user.id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.get("/recommendations", response_model=List[schemas.RecommendationResponse])
def get_recommendations(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    recommendations = db.query(models.Recommendation).filter(models.Recommendation.user_id == current_user.id).all()
    return recommendations
