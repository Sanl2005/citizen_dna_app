from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    full_name: str
    password: str
    phone: Optional[str] = None
    role: str = "citizen" # citizen, admin

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class SchemeBase(BaseModel):
    scheme_name: str
    ministry: str
    description: str
    benefits: str
    eligibility_rules: str
    min_age: Optional[int] = None
    max_income: Optional[float] = None
    required_gender: Optional[str] = None
    apply_url: Optional[str] = None
    category: Optional[str] = None

class SchemeCreate(SchemeBase):
    pass

class Scheme(SchemeBase):
    id: int
    class Config:
        orm_mode = True

class ProfileBase(BaseModel):
    age: int
    gender: str
    income: float
    education: str
    occupation: str
    employment_status: str
    location_state: str
    location_district: str
    area_of_residence: str = "Urban"
    community: Optional[str] = None
    disability_status: bool
    family_size: int
    single_parent_child: str = "No"
    is_student: str = "No"
    
    marriage_cert: Optional[str] = None
    divorce_cert: Optional[str] = None
    widow_cert: Optional[str] = None
    community_cert: Optional[str] = None
    aadhar_card: Optional[str] = None
    income_cert: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    risk_score_health: float
    risk_score_financial: float
    class Config:
        orm_mode = True

class RecommendationBase(BaseModel):
    scheme_id: int
    confidence_score: float
    reason: str

class RecommendationResponse(RecommendationBase):
    id: int
    scheme: Scheme
    class Config:
        orm_mode = True

class ChatMessageRequest(BaseModel):
    message: str
