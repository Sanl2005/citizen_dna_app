import sqlite3
import os

db_path = os.path.join("backend", "citizen_dna.db")
if not os.path.exists(db_path):
    print("Database not found")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, full_name FROM users")
    users = cursor.fetchall()
    print("USERS IN DATABASE:")
    for user in users:
        print(f"ID: {user[0]}, Email: {user[1]}, Name: {user[2]}")
    conn.close()
