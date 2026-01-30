from database import SessionLocal
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

# Create test users
users_to_create = [
    {
        "email": "santhosh@gmail.com",
        "full_name": "Santhosh",
        "password": "password",
        "phone": "1234567890"
    },
    {
        "email": "san@gmail.com",
        "full_name": "San",
        "password": "password",
        "phone": "9876543210"
    },
    {
        "email": "test@gmail.com",
        "full_name": "Test User",
        "password": "password",
        "phone": "5555555555"
    }
]

for user_data in users_to_create:
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_data["email"]).first()
    if existing:
        print(f"⚠ User {user_data['email']} already exists, skipping")
        continue
    
    # Create new user
    hashed_password = pwd_context.hash(user_data["password"])
    new_user = User(
        email=user_data["email"],
        full_name=user_data["full_name"],
        hashed_password=hashed_password,
        phone=user_data["phone"],
        role="citizen"
    )
    db.add(new_user)
    print(f"✓ Created user: {user_data['email']} (password: {user_data['password']})")

db.commit()
db.close()

print("\n✓ All users created successfully!")
