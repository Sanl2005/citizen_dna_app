import sqlite3
import os

db_path = os.path.join("backend", "citizen_dna.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE citizen_profiles ADD COLUMN location_type VARCHAR(50) DEFAULT 'Urban'")
    print("Added location_type")
except Exception as e:
    print(f"location_type likely exists: {e}")

try:
    cursor.execute("ALTER TABLE citizen_profiles ADD COLUMN community VARCHAR(100)")
    print("Added community")
except Exception as e:
    print(f"community likely exists: {e}")

conn.commit()
conn.close()
