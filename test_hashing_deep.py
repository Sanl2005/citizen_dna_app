from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = "test"
try:
    hashed = pwd_context.hash(password)
    print(f"HASHED: {hashed}")
    verified = pwd_context.verify(password, hashed)
    print(f"VERIFIED: {verified}")
except Exception as e:
    print(f"ERROR: {e}")
