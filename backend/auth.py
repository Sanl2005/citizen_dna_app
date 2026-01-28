from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database
import models

# Secret key for JWT (should be Env Var in production)
SECRET_KEY = "HACKATHON_DEMO_SECRET_KEY_PLEASE_CHANGE_IN_PROD"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):
    try:
        # Bcrypt has a 72-byte limit. Truncate to be safe and avoid ValueError.
        # This handles the limit consistently across different library versions.
        safe_password = str(password)[:72]
        return pwd_context.hash(safe_password)
    except Exception as e:
        print(f"CRITICAL: Hashing failed: {e}")
        # Fallback to a simple hash for demo purposes if bcrypt fails
        import hashlib
        return "sha256:" + hashlib.sha256(str(password).encode()).hexdigest()

def verify_password(plain_password, hashed_password):
    try:
        if str(hashed_password).startswith("sha256:"):
            import hashlib
            expected = "sha256:" + hashlib.sha256(str(plain_password).encode()).hexdigest()
            return expected == hashed_password
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"CRITICAL: Verification failed: {e}")
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # print(f"DEBUG: Decoding token: {token[:15]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            print("ERROR: Token payload 'sub' is missing")
            raise credentials_exception
    except JWTError as e:
        print(f"ERROR: JWT Decode failed: {str(e)}")
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        print(f"ERROR: User {email} in token not found in DB")
        raise credentials_exception
        
    return user
