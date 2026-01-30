from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    hashed_password = Column(String(255))
    role = Column(String(50), default="citizen") # citizen, admin, policymaker
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    profile = relationship("CitizenProfile", back_populates="user", uselist=False)
    recommendations = relationship("Recommendation", back_populates="user")


class CitizenProfile(Base):
    __tablename__ = "citizen_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    age = Column(Integer)
    gender = Column(String(50))
    income = Column(Float)
    education = Column(String(100))
    occupation = Column(String(100))
    location_state = Column(String(100))
    location_district = Column(String(100))
    location_type = Column(String(50), default="Urban") # Deprecated, use area_of_residence
    area_of_residence = Column(String(50), default="Urban")
    
    community = Column(String(100), nullable=True) # SC, ST, OBC, General
    # Disability status, family size, etc.
    disability_status = Column(Boolean, default=False)
    family_size = Column(Integer, default=1)
    
    # New Fields
    employment_status = Column(String(100), default="Unemployed")
    is_student = Column(String(50), default="No")
    single_parent_child = Column(String(50), default="No")
    
    # Documents (Filenames only for now)
    marriage_cert = Column(String(255), nullable=True)
    divorce_cert = Column(String(255), nullable=True)
    widow_cert = Column(String(255), nullable=True)
    community_cert = Column(String(255), nullable=True)
    aadhar_card = Column(String(255), nullable=True)
    income_cert = Column(String(255), nullable=True)

    # Calculated risk score from AI
    minority_status = Column(String(50), default="No")
    risk_score_health = Column(Float, default=0.0)
    risk_score_financial = Column(Float, default=0.0)
    
    digital_dna_vector = Column(Text) # JSON string of vector representation

    user = relationship("User", back_populates="profile")


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    scheme_name = Column(String(255), index=True)
    ministry = Column(String(255))
    description = Column(Text)
    eligibility_rules = Column(Text) # Could be JSON or text description
    benefits = Column(Text)
    
    # For simple rule-based filtering
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    max_income = Column(Float, nullable=True)
    required_gender = Column(String(50), nullable=True)
    apply_url = Column(String(500), nullable=True)
    category = Column(String(100), nullable=True)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scheme_id = Column(Integer, ForeignKey("schemes.id"))
    
    confidence_score = Column(Float)
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="recommendations")
    scheme = relationship("Scheme")
