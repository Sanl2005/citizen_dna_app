
import database
import models
from sqlalchemy.orm import Session

db = database.SessionLocal()
schemes = db.query(models.Scheme).all()

print(f"Total schemes: {len(schemes)}")
for s in schemes:
    print(f"ID: {s.id}, Name: {s.scheme_name}, Category: {s.category}")

db.close()
