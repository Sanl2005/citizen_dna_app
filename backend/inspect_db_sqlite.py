
import sqlite3
import os

# Check which DB file exists
db_files = [f for f in os.listdir('.') if f.endswith('.db')]
print(f"Found DB files: {db_files}")

# Assuming v5 is the one used based on database.py
db_path = "G:/citizen_dna_app/backend/citizen_dna_v6.db"
if not os.path.exists(db_path):
    print(f"DB {db_path} not found!")

print(f"Inspecting {db_path}...")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT id, scheme_name, category FROM schemes LIMIT 20")
    rows = cursor.fetchall()
    print(f"\nTotal rows fetched: {len(rows)}")
    for row in rows:
        print(row)
except Exception as e:
    print(f"Error: {e}")

conn.close()
