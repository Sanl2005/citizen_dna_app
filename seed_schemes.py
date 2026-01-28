import sqlite3
import os

db_path = os.path.join("backend", "citizen_dna.db")
if not os.path.exists(db_path):
    # Fallback for if run from inside backend folder
    db_path = "citizen_dna.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sample Schemes Data with Categories
# Columns: Name, Ministry, Description, Eligibility, Benefits, Min Age, Max Income, Gender, URL, Category
schemes = [
    # HOUSING
    ("Pradhan Mantri Awas Yojana (Rural)", "Ministry of Rural Development", "Housing for all in rural areas. Special preference for SC/ST and women.", "Live in rural area, BPL status", "₹1.2 Lakh subsidy", None, 150000.0, None, "https://pmaymis.gov.in/", "Housing"),
    ("Pradhan Mantri Gramin Awaas Yojana", "Ministry of Rural Development", "Providing houses to the houseless and those living in dilapidated houses in rural areas.", "Rural BPL, SC/ST, widows", "Financial assistance for house construction", 18, 150000.0, None, "https://pmayg.nic.in/", "Housing"),
    
    # AGRICULTURE
    ("PM-KISAN", "Ministry of Agriculture", "Direct income support for farmers.", "Small/marginal landholder", "₹6000 per year", 18, 200000.0, None, "https://pmkisan.gov.in/", "Agriculture"),
    ("Agri-Clinics and Agri-Business Centres", "Ministry of Agriculture", "Self-employment opportunities to unemployed agricultural graduates.", "Agri graduates", "Back-ended composite subsidy", 18, None, None, "https://www.agriclinics.net/", "Agriculture"),
    
    # WOMEN
    ("Sukanya Samriddhi Yojana", "Ministry of Women & Child Development", "Savings scheme for girl child.", "Parent of girl child", "High interest rate", None, None, "Female", "https://www.indiapost.gov.in/Financial/Pages/Content/Post-Office-Saving-Schemes.aspx", "Women"),
    ("Ujjwala Yojana", "Ministry of Petroleum", "Free LPG connection for BPL households. Preference for rural women.", "BPL card holder, Female head", "Free LPG connection", 18, 100000.0, "Female", "https://www.pmuy.gov.in/", "Women"),
    ("Janani Suraksha Yojana", "Ministry of Health", "Reducing maternal and neonatal mortality among poor pregnant women.", "Low income mothers", "Cash assistance for delivery", 19, 50000.0, "Female", "https://nhm.gov.in/jsy.php", "Women"), # Also Health
    
    # HEALTH
    ("National Health Mission", "Ministry of Health", "Accessible and affordable healthcare for all. High priority for rural populations.", "All citizens", "Free diagnostics and medicines", None, None, None, "https://nhm.gov.in/", "Health"),
    ("Ayushman Bharat (PM-JAY)", "Ministry of Health", "World's largest health insurance scheme providing ₹5 lakh per family.", "Low income, listed in SECC", "₹5 Lakh health cover", None, 100000.0, None, "https://pmjay.gov.in/", "Health"),
    
    # EDUCATION
    ("Post Matric Scholarship for SC Students", "Ministry of Social Justice", "Financial assistance to SC students for post-matric studies.", "Continuous education, SC community", "Full tuition fee waiver", 15, 250000.0, None, "https://scholarships.gov.in/", "Education"),
    ("National Fellowship for OBC Students", "Ministry of Social Justice", "Fellowship for students from Other Backward Classes pursuing higher education.", "OBC community, pursuing MPhil/PhD", "Monthly stipend", 22, 600000.0, None, "https://socialjustice.gov.in/", "Education"),
    ("PMGDISHA", "Ministry of Electronics & IT", "Making 6 crore citizens in rural India digitally literate.", "Rural residents, age 18-60", "Digital literacy certification", 18, None, None, "https://www.pmgdisha.in/", "Education"),
    
    # FINANCE & EMPLOYMENT
    ("Skill India Mission", "Ministry of Skill Development", "Training for youth to get jobs. Open to all communities.", "Youth seeking skills", "Certified training & job support", 18, None, None, "https://www.skillindia.gov.in/", "Finance"),
    ("Start-up Village Entrepreneurship Programme", "Ministry of Rural Development", "Support for rural startups and enterprises.", "Rural resident, age 18-45", "Capital support and mentorship", 18, 300000.0, None, "https://nrlm.gov.in/", "Finance"),
    ("Stand-Up India", "Ministry of Finance", "Loans for SC/ST and Women entrepreneurs to set up greenfield enterprises.", "SC/ST or Women", "₹10 Lakh to ₹100 Lakh loan", 18, None, None, "https://www.standupmitra.in/", "Finance"),
    ("Pradhan Mantri Mudra Yojana", "Ministry of Finance", "Refinance support for small businesses in non-farm sector.", "Micro entrepreneurs", "Loans up to ₹10 Lakh", 18, 1200000.0, None, "https://www.mudra.org.in/", "Finance"),
    ("Pradhan Mantri Shram Yogi Maandhan (PM-SYM)", "Ministry of Labour", "Pension scheme for unorganised workers.", "Unorganised workers, income < ₹15,000", "Monthly pension of ₹3,000 after age 60", 18, 180000.0, None, "https://maandhan.in/", "Finance"),
    ("Van Dhan Yojana", "Ministry of Tribal Affairs", "Livelihood generation for tribals by harnessing forest wealth.", "Tribal communities, SHGs", "Training and value addition support", 18, None, None, "https://trifed.tribal.gov.in/", "Finance"),
    ("Atal Pension Yojana", "Ministry of Finance", "Pension scheme for all citizens in the unorganised sector.", "Age 18-40", "Guaranteed pension after 60", 18, None, None, "https://www.npscra.nsdl.co.in/scheme-details.php", "Finance")
]

# Drop existing table to ensure schema update
cursor.execute("DROP TABLE IF EXISTS schemes")

# Create table
cursor.execute('''
    CREATE TABLE schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scheme_name VARCHAR(255),
        ministry VARCHAR(255),
        description TEXT,
        eligibility_rules TEXT,
        benefits TEXT,
        min_age INTEGER,
        max_income FLOAT,
        required_gender VARCHAR(50),
        apply_url VARCHAR(500),
        category VARCHAR(100)
    )
''')

# Clear existing schemes
cursor.execute("DELETE FROM schemes")

# Insert
cursor.executemany('''
    INSERT INTO schemes (scheme_name, ministry, description, eligibility_rules, benefits, min_age, max_income, required_gender, apply_url, category)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', schemes)

conn.commit()
conn.close()
print(f"Seeded {len(schemes)} categorized schemes successfully.")
