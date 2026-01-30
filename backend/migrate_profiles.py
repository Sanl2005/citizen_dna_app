import sqlite3

# Connect to the database
db_path = 'citizen_dna_v7.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def add_column_if_not_exists(table, column, type):
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type}")
        print(f"✓ Added column {column} to {table}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"- Column {column} already exists in {table}")
        else:
            print(f"Error adding {column}: {e}")

# Add new certificate columns
add_column_if_not_exists("citizen_profiles", "disability_cert", "VARCHAR(255)")
add_column_if_not_exists("citizen_profiles", "education_cert", "VARCHAR(255)")
add_column_if_not_exists("citizen_profiles", "bpl_cert", "VARCHAR(255)")

conn.commit()
conn.close()
print("\n✓ Database migration completed successfully")
