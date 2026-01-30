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
        "employment_status": db_profile.employment_status,
        "is_student": db_profile.is_student, # Now explicit
        "location_state": db_profile.location_state,
        "area_of_residence": db_profile.area_of_residence, # Renamed from location_type
        "community": db_profile.community,
        "gender": db_profile.gender
    }
    
    # Calculate Component Risks explicitly for better UI accuracy
    h_score = ai_engine.calculate_health_risk(ai_input)
    f_score = ai_engine.calculate_financial_risk(ai_input)
    
    db_profile.risk_score_health = h_score
    db_profile.risk_score_financial = f_score
    
    # Use average for scheme boosting logic
    score = (h_score + f_score) / 2

    
    # Generate Real-time Recommendations
    # 1. Clear old recommendations
    db.query(models.Recommendation).filter(models.Recommendation.user_id == current_user.id).delete()
    
    # 2. Match with available schemes
    all_schemes = db.query(models.Scheme).all()
    for s in all_schemes:
        # --- Strict Exclusion Criteria (Hard Filters) ---
        
        # 1. Gender Filter (Enhanced)
        user_g = (db_profile.gender or "").lower()
        req_g = (s.required_gender or "").lower()
        
        # Check explicit requirements
        if user_g == "male":
            if req_g in ["female", "woman", "women"]:
                continue
            # Additional check: If Scheme Category or Name suggests it's for women
            # (e.g. "Mahila Samman", "Maternity Benefit", Category="Women Empowerment")
            check_text = ((s.category or "") + " " + (s.scheme_name or "")).lower()
            if any(w in check_text for w in ["women", "woman", "female", "girl", "daughter", "maternity", "widow", "mahila", "nari", "sister", "mother"]):
                continue

        if user_g == "female":
            if req_g in ["male", "man", "men"]:
                continue

        # 2. Age Filter (Strict)
        if s.min_age and db_profile.age < s.min_age:
            continue
        
        if s.max_age and db_profile.age > s.max_age:
            continue
            
        # 3. Income Filter (Strict)
        if s.max_income and db_profile.income > s.max_income:
            continue

        # 4. Occupation Filter (Heuristic)
        scheme_text = ((s.scheme_name or "") + " " + (s.description or "") + " " + (s.eligibility_rules or "")).lower()
        
        # Farmer Check
        if any(x in scheme_text for x in ["kisan", "farmer", "agriculture", "krishi", "crop insurance"]):
            user_occ = (db_profile.occupation or "").lower()
            is_farmer = any(x in user_occ for x in ["farmer", "agriculture", "cultivator"])
            if not is_farmer: continue

        # Street Vendor Check (PM SVANidhi)
        if "street vendor" in scheme_text or "svanidhi" in scheme_text:
             user_occ = (db_profile.occupation or "").lower()
             if "vendor" not in user_occ and "hawker" not in user_occ: continue
             
        # 5. Student / Education Filter (Strict)
        if any(x in scheme_text for x in ["student", "scholarship", "fellowship", "matric", "university", "college"]):
            # Must be a student
            if (db_profile.is_student or "No") == "No": 
                continue

        # 6. Community / Social Category Filter (Strict)
        # Define user status
        user_comm = (db_profile.community or "General").lower()
        is_minority = (db_profile.minority_status or "No") == "Yes"
        
        # Check for SC requirements
        if "sc " in scheme_text or "scheduled caste" in scheme_text:
            if "sc" not in user_comm: continue
            
        # Check for ST requirements
        if "st " in scheme_text or "scheduled tribe" in scheme_text:
            if "st" not in user_comm: continue
            
        # Check for OBC requirements
        if "obc" in scheme_text or "backward class" in scheme_text:
            if "obc" not in user_comm: continue
            
        # Check for Minority requirements
        if "minority" in scheme_text:
            if not is_minority: continue

        # --- Matching Logic (Positive Signals) ---
        match = False
        reasons = []
        
        # Simple Logic Engine
        # If filters pass, we check for positive indicators to confirm match
        
        # Age eligibility (already passed filter, but adds to reason)
        if s.min_age and db_profile.age >= s.min_age:
            reasons.append(f"Eligible for age {db_profile.age}")
            
        # Income eligibility
        if s.max_income and db_profile.income <= s.max_income:
            reasons.append(f"Income ₹{db_profile.income} fits limit")
            
        # Gender eligibility
        if s.required_gender and (db_profile.gender or "").lower() == s.required_gender.lower():
            match = True # Strong match
            reasons.append(f"Dedicated benefit for {db_profile.gender}")
            
        # Location/Rural
        if s.description and "Rural" in s.description and db_profile.location_type == "Rural":
            match = True
            reasons.append("Rural area support")

        # Community Specific
        if db_profile.community and (db_profile.community in (s.scheme_name or "") or db_profile.community in (s.description or "")):
            match = True
            reasons.append(f"Targeted for {db_profile.community} category")

        # Occupation Specific (Farmer/Vendor/Student already filtered, so here we confirm match)
        if "student" in scheme_text and db_profile.is_student == "Yes":
            match = True
            reasons.append("Student benefit")
            
        if "agriculture" in scheme_text and "farmer" in (db_profile.occupation or "").lower():
            match = True
            reasons.append("Farmer benefit")
            
        # Score Logic - Only boost if passes basics
        if score > 0.6: 
             # Only auto-match high risk if it's a general welfare scheme or health scheme
             if s.category in ["Health", "Pension", "Housing", "Rural Development"]:
                 match = True
                 reasons.append("High priority welfare match")

        # General "All" match fallback if no specific exclusions triggered and it's a generic category
        # E.g. Skill Development is often open to all if age fits
        if not match and s.category in ["Skill Development", "Health", "Employment"]:
            # If no hard blocks were hit, these are generally applicable
            match = True
            reasons.append(f"General eligibility for {s.category}")

        if match:
             # Boost confidence
            confidence = 0.8 + (score * 0.1)
            
            new_rec = models.Recommendation(
                user_id=current_user.id,
                scheme_id=s.id,
                confidence_score=min(confidence, 0.99),
                reason=" and ".join(reasons[:2]) or "AI predicted match based on profile"
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
