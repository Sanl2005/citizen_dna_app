import sqlite3
import os

db_path = "citizen_dna.db"
if not os.path.exists(db_path):
    print("Root Database not found")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"TABLES IN ROOT DB: {tables}")
    try:
        cursor.execute("SELECT id, email, full_name FROM users")
        users = cursor.fetchall()
        print("USERS IN ROOT DB:")
        for user in users:
            print(f"ID: {user[0]}, Email: {user[1]}, Name: {user[2]}")
    except:
        print("No users table in root DB")
    conn.close()
