import sqlite3
import os

db_path = os.path.join("backend", "citizen_dna.db")
if not os.path.exists(db_path):
    # Fallback for if run from inside backend folder
    db_path = "citizen_dna.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sample Schemes Data with more variety
schemes = [
    ("Pradhan Mantri Awas Yojana (Rural)", "Ministry of Rural Development", "Housing for all in rural areas. Special preference for SC/ST and women.", "Live in rural area, BPL status", "₹1.2 Lakh subsidy", None, 150000.0, None),
    ("PM-KISAN", "Ministry of Agriculture", "Direct income support for farmers.", "Small/marginal landholder", "₹6000 per year", 18, 200000.0, None),
    ("Sukanya Samriddhi Yojana", "Ministry of Women & Child Development", "Savings scheme for girl child.", "Parent of girl child", "High interest rate", None, None, "Female"),
    ("Old Age Pension Scheme", "Ministry of Social Justice", "Monthly pension for senior citizens.", "Age > 60", "₹1000 - ₹3000 per month", 60, 50000.0, None),
    ("Skill India Mission", "Ministry of Skill Development", "Training for youth to get jobs. Open to all communities.", "Youth seeking skills", "Certified training & job support", 18, None, None),
    ("Post Matric Scholarship for SC Students", "Ministry of Social Justice", "Financial assistance to SC students for post-matric studies.", "Continuous education, SC community", "Full tuition fee waiver", 15, 250000.0, None),
    ("National Fellowship for OBC Students", "Ministry of Social Justice", "Fellowship for students from Other Backward Classes pursuing higher education.", "OBC community, pursuing MPhil/PhD", "Monthly stipend", 22, 600000.0, None),
    ("Ujjwala Yojana", "Ministry of Petroleum", "Free LPG connection for BPL households. Preference for rural women.", "BPL card holder, Female head", "Free LPG connection", 18, 100000.0, "Female"),
    ("Start-up Village Entrepreneurship Programme", "Ministry of Rural Development", "Support for rural startups and enterprises.", "Rural resident, age 18-45", "Capital support and mentorship", 18, 300000.0, None),
    ("National Health Mission", "Ministry of Health", "Accessible and affordable healthcare for all. High priority for rural populations.", "All citizens", "Free diagnostics and medicines", None, None, None),
    ("Stand-Up India", "Ministry of Finance", "Loans for SC/ST and Women entrepreneurs to set up greenfield enterprises.", "SC/ST or Women", "₹10 Lakh to ₹100 Lakh loan", 18, None, None),
    ("Janani Suraksha Yojana", "Ministry of Health", "Reducing maternal and neonatal mortality among poor pregnant women.", "Low income mothers", "Cash assistance for delivery", 19, 50000.0, "Female"),
    ("Pradhan Mantri Mudra Yojana", "Ministry of Finance", "Refinance support for small businesses in non-farm sector.", "Micro entrepreneurs", "Loans up to ₹10 Lakh", 18, 1200000.0, None)
]

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scheme_name VARCHAR(255),
        ministry VARCHAR(255),
        description TEXT,
        eligibility_rules TEXT,
        benefits TEXT,
        min_age INTEGER,
        max_income FLOAT,
        required_gender VARCHAR(50)
    )
''')

# Clear existing schemes
cursor.execute("DELETE FROM schemes")

# Insert
cursor.executemany('''
    INSERT INTO schemes (scheme_name, ministry, description, eligibility_rules, benefits, min_age, max_income, required_gender)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', schemes)

conn.commit()
conn.close()
print("Comprehensive sample schemes seeded successfully.")
