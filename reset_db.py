import sqlite3
import os

db_path = os.path.join("backend", "citizen_dna.db")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM citizen_profiles")
    cursor.execute("DELETE FROM recommendations")
    cursor.execute("DELETE FROM schemes")
    conn.commit()
    conn.close()
    print("DATABASE CLEARED SUCCESSFULLY")
else:
    print("Database not found")
