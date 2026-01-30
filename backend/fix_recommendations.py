import sqlite3

# Connect to the database
db_path = 'citizen_dna_v7.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop and recreate recommendations table
cursor.execute('DROP TABLE IF EXISTS recommendations')
cursor.execute('''
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    scheme_id INTEGER NOT NULL,
    confidence_score FLOAT,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (scheme_id) REFERENCES schemes(id)
)
''')

conn.commit()
conn.close()
print("✓ Recommendations table recreated")
