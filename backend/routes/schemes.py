from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database, models, schemas, auth

router = APIRouter(
    prefix="/schemes",
    tags=["Schemes"]
)

@router.get("/", response_model=List[schemas.Scheme])
def read_schemes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    schemes = db.query(models.Scheme).offset(skip).limit(limit).all()
    return schemes

@router.post("/", response_model=schemas.Scheme)
def create_scheme(
    scheme: schemas.SchemeCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    # Ideally check if user is admin
    # if current_user.role != "admin": raise HTTPException...
    db_scheme = models.Scheme(**scheme.dict())
    db.add(db_scheme)
    db.commit()
    db.refresh(db_scheme)
    return db_scheme
