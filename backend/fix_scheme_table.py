import sqlite3
import os

# Connect to the database
db_path = 'citizen_dna_v7.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop the old schemes table and recreate with proper column size
cursor.execute('DROP TABLE IF EXISTS schemes')
cursor.execute('''
CREATE TABLE schemes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_name VARCHAR(255),
    ministry VARCHAR(255),
    description TEXT,
    eligibility_rules TEXT,
    benefits TEXT,
    min_age INTEGER,
    max_age INTEGER,
    max_income FLOAT,
    required_gender VARCHAR(50),
    apply_url VARCHAR(500),
    category VARCHAR(255)
)
''')

conn.commit()
conn.close()
print("✓ Schemes table recreated with proper category column size")
