import sqlite3
import os

db_path = os.path.join("backend", "citizen_dna.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(citizen_profiles)")
cols = cursor.fetchall()
for col in cols:
    print(col[1])
conn.close()
