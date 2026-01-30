import database
import models
from sqlalchemy.orm import Session

# Initialize DB Session
models.Base.metadata.create_all(bind=database.engine)
db = database.SessionLocal()

def seed_schemes():
    # Clear existing schemes to avoid duplicates
    db.query(models.Scheme).delete()
    
    schemes_data = [
        # --- FARMERS / AGRICULTURE ---
        {
            "scheme_name": "PM-KISAN",
            "ministry": "Ministry of Agriculture",
            "description": "Income support of Rs 6000 per year to all land holding farmer families.",
            "eligibility_rules": "All land holding farmers. Excludes institutional land holders and high income earners.",
            "benefits": "Rs. 6000 per annum in 3 installments.",
            "min_age": 18,
            "max_age": None,
            "max_income": None, 
            "required_gender": None,
            "category": "Agriculture",
            "apply_url": "https://www.myscheme.gov.in/schemes/pm-kisan"
        },
        {
            "scheme_name": "Pradhan Mantri Fasal Bima Yojana",
            "ministry": "Ministry of Agriculture",
            "description": "Crop insurance scheme to provide financial support to farmers suffering crop loss/damage.",
            "eligibility_rules": "Farmers growing notified crops in notified areas.",
            "benefits": "Insurance coverage and financial support.",
            "min_age": 18,
            "max_age": None,
            "max_income": None,
            "required_gender": None,
            "category": "Agriculture",
            "apply_url": "https://www.myscheme.gov.in/schemes/pmfby"
        },
        {
            "scheme_name": "Kisan Credit Card (KCC)",
            "ministry": "Ministry of Finance",
            "description": "Adequate and timely credit support from the banking system for cultivation and other needs.",
            "eligibility_rules": "Farmers, tenant farmers, oral lessees, share croppers.",
            "benefits": "Credit at affordable rates.",
            "min_age": 18,
            "max_age": None,
            "max_income": None,
            "required_gender": None,
            "category": "Agriculture",
            "apply_url": "https://www.myscheme.gov.in/schemes/kcc"
        },

        # --- STUDENTS / EDUCATION ---
        {
            "scheme_name": "Post Matric Scholarship for SC Students",
            "ministry": "Ministry of Social Justice",
            "description": "Financial assistance to SC students for studying at post-matriculation or post-secondary stage.",
            "eligibility_rules": "SC students only. Annual parental income < Rs 2.5 Lakhs.",
            "benefits": "Maintenance allowance, reimbursement of compulsory non-refundable fees.",
            "min_age": 16,
            "max_age": 30, # Implied cap for students
            "max_income": 250000,
            "required_gender": None,
            "category": "Education",
            "apply_url": "https://scholarships.gov.in/"
        },
        {
            "scheme_name": "National Fellowship for OBC Students",
            "ministry": "Ministry of Social Justice",
            "description": "Fellowship to OBC students for pursuing M.Phil and Ph.D.",
            "eligibility_rules": "OBC students. Parental income < Rs 6 Lakhs.",
            "benefits": "Fellowship amount similar to JRF/SRF.",
            "min_age": 21,
            "max_age": 35,
            "max_income": 600000,
            "required_gender": None,
            "category": "Education",
            "apply_url": "https://scholarships.gov.in/"
        },
        {
            "scheme_name": "Central Sector Scheme of Scholarship for College and University Students",
            "ministry": "Ministry of Education",
            "description": "Scholarship for meritorious students from low income families.",
            "eligibility_rules": "Above 80th percentile in Class 12. Income < Rs 8 Lakhs.",
            "benefits": "Rs 10,000 to Rs 20,000 per annum.",
            "min_age": 17,
            "max_age": 25,
            "max_income": 800000,
            "required_gender": None,
            "category": "Education",
            "apply_url": "https://scholarships.gov.in/"
        },

        # --- WOMEN / MATERNITY ---
        {
            "scheme_name": "Pradhan Mantri Matru Vandana Yojana (PMMVY)",
            "ministry": "Ministry of Women and Child Development",
            "description": "Maternity benefit program providing cash incentive for partial compensation of wage loss.",
            "eligibility_rules": "Pregnant Women and Lactating Mothers (PW&LM) for first living child of the family.",
            "benefits": "Rs 5,000 in 3 installments.",
            "min_age": 19,
            "max_age": 45, # Childbearing age approx
            "max_income": None,
            "required_gender": "Female",
            "category": "Women Welfare",
            "apply_url": "https://www.myscheme.gov.in/schemes/pmmvy"
        },
        {
            "scheme_name": "Janani Suraksha Yojana",
            "ministry": "Ministry of Health",
            "description": "Safe motherhood intervention under NHM. Promotes institutional delivery.",
            "eligibility_rules": "Pregnant women, focusing on poor/rural.",
            "benefits": "Cash assistance for institutional delivery.",
            "min_age": 19,
            "max_age": 45,
            "max_income": None, 
            "required_gender": "Female",
            "category": "Women Welfare",
            "apply_url": "https://wd.gov.in/jsy"
        },
        {
            "scheme_name": "Sukanya Samriddhi Yojana",
            "ministry": "Ministry of Finance",
            "description": "Small deposit scheme for the girl child.",
            "eligibility_rules": "Girl child below 10 years of age.",
            "benefits": "High interest rate, tax benefits.",
            "min_age": 0,
            "max_age": 10, # Strict upper limit
            "max_income": None,
            "required_gender": "Female",
            "category": "Women Welfare",
            "apply_url": "https://www.myscheme.gov.in/schemes/ssy"
        },

        # --- HEALTH ---
        {
            "scheme_name": "Ayushman Bharat (PM-JAY)",
            "ministry": "Ministry of Health",
            "description": "World's largest health insurance/assurance scheme.",
            "eligibility_rules": "Poor and vulnerable families listed in SECC 2011.",
            "benefits": "Cover of Rs 5 Lakhs per family per year for secondary and tertiary care hospitalization.",
            "min_age": None,
            "max_age": None,
            "max_income": None, 
            "required_gender": None,
            "category": "Health",
            "apply_url": "https://www.myscheme.gov.in/schemes/ayushman-bharat-pradhan-mantri-jan-arogya-yojana"
        },
        {
            "scheme_name": "Pradhan Mantri Suraksha Bima Yojana",
            "ministry": "Ministry of Finance",
            "description": "Accident Insurance Scheme.",
            "eligibility_rules": "Age 18-70 years with bank account.",
            "benefits": "Rs 2 Lakhs for accidental death and full disability.",
            "min_age": 18,
            "max_age": 70,
            "max_income": None,
            "required_gender": None,
            "category": "Health",
            "apply_url": "https://www.myscheme.gov.in/schemes/pmsby"
        },
        {
            "scheme_name": "Aam Aadmi Bima Yojana",
            "ministry": "Ministry of Finance",
            "description": "Social security for rural landless households.",
            "eligibility_rules": "Head of rural landless household, age 18-59.",
            "benefits": "Insurance cover for death and disability.",
            "min_age": 18,
            "max_age": 59,
            "max_income": None,
            "required_gender": None,
            "category": "Health",
            "apply_url": "https://financialservices.gov.in/insurance-divisions/Social-Security-Schemes/Aam-Admi-Bima-Yojana"
        },

        # --- HOUSING / RURAL DEV ---
        {
            "scheme_name": "Pradhan Mantri Awas Yojana (Rural)",
            "ministry": "Ministry of Rural Development",
            "description": "Housing for all in rural areas.",
            "eligibility_rules": "Homeless and those living in dilapidated houses in rural areas.",
            "benefits": "Financial assistance for construction of pucca house.",
            "min_age": None,
            "max_age": None,
            "max_income": 300000,
            "required_gender": None,
            "category": "Housing",
            "apply_url": "https://www.myscheme.gov.in/schemes/pmayg"
        },
        {
            "scheme_name": "Pradhan Mantri Gram Sadak Yojana",
            "ministry": "Ministry of Rural Development",
            "description": "Connectivity to unconnected habitations.",
            "eligibility_rules": "Rural habitations.",
            "benefits": "All weather road connectivity.",
            "min_age": None,
            "max_age": None,
            "max_income": None,
            "required_gender": None,
            "category": "Rural Development",
            "apply_url": "https://omms.nic.in/"
        },
        {
            "scheme_name": "Deen Dayal Antyodaya Yojana (NRLM)",
            "ministry": "Ministry of Rural Development",
            "description": "Poverty alleviation through building strong institutions of the poor.",
            "eligibility_rules": "Rural poor households.",
            "benefits": "Self-employment training, bank linkage.",
            "min_age": 18,
            "max_age": 60,
            "max_income": None,
            "required_gender": None,
            "category": "Rural Development",
            "apply_url": "https://aajeevika.gov.in/"
        },

        # --- EMPLOYMENT / SKILLS ---
        {
            "scheme_name": "Pradhan Mantri Kaushal Vikas Yojana",
            "ministry": "Ministry of Skill Development",
            "description": "Skill certification scheme to enable youth to take up industry-relevant skill training.",
            "eligibility_rules": "Indian youth, dropouts.",
            "benefits": "Short term training, recognition of prior learning.",
            "min_age": 15,
            "max_age": 29, # Strict youth definition often applied
            "max_income": None,
            "required_gender": None,
            "category": "Skill Development",
            "apply_url": "https://www.myscheme.gov.in/schemes/pmkvy-4.0"
        },
        {
            "scheme_name": "MGNREGA",
            "ministry": "Ministry of Rural Development",
            "description": "Guarantees 100 days of wage employment in a financial year to a rural household.",
            "eligibility_rules": "Rural households willing to do unskilled manual work.",
            "benefits": "Guaranteed wage employment.",
            "min_age": 18,
            "max_age": None,
            "max_income": None,
            "required_gender": None,
            "category": "Employment",
            "apply_url": "https://nrega.nic.in/"
        },
        {
            "scheme_name": "Deen Dayal Upadhyaya Grameen Kaushalya Yojana",
            "ministry": "Ministry of Rural Development",
            "description": "Demand-driven placement linked skill training.",
            "eligibility_rules": "Rural youth 15-35 years.",
            "benefits": "Skill training and placement.",
            "min_age": 15,
            "max_age": 35, # Explicit
            "max_income": None,
            "required_gender": None,
            "category": "Skill Development",
            "apply_url": "https://www.myscheme.gov.in/schemes/ddugky"
        },
        
         # --- SMALL BUSINESS ---
        {
            "scheme_name": "Pradhan Mantri Mudra Yojana",
            "ministry": "Ministry of Finance",
            "description": "To provide loans up to 10 Lakhs to non-corporate, non-farm small/micro enterprises.",
            "eligibility_rules": "Any Indian Citizen who has a business plan for non-farm sector income generating activity.",
            "benefits": "Loans up to 10 Lakhs (Shishu, Kishore, Tarun).",
            "min_age": 18,
            "max_age": 65,
            "max_income": None,
            "required_gender": None,
            "category": "Business",
            "apply_url": "https://www.myscheme.gov.in/schemes/pmmy"
        },
        {
            "scheme_name": "Stand-Up India",
            "ministry": "Ministry of Finance",
            "description": "Bank loans between 10 lakh and 1 Crore to SC/ST or Women borrowers.",
            "eligibility_rules": "SC/ST and/or Woman entrepreneur, above 18 years.",
            "benefits": "Loan for greenfield enterprise.",
            "min_age": 18,
            "max_age": None,
            "max_income": None,
            "required_gender": None, 
            "category": "Business",
            "apply_url": "https://www.myscheme.gov.in/schemes/standup-india"
        },
        {
            "scheme_name": "PM SVANidhi",
            "ministry": "Ministry of Housing and Urban Affairs",
            "description": "Micro credit scheme for street vendors.",
            "eligibility_rules": "Street vendors in urban areas.",
            "benefits": "Collateral free working capital loan up to Rs 10,000.",
            "min_age": 18,
            "max_age": None,
            "max_income": None,
            "required_gender": None,
            "category": "Business",
            "apply_url": "https://www.myscheme.gov.in/schemes/pm-svanidhi"
        },

        # --- FINANCIAL / PENSION ---
        {
            "scheme_name": "Atal Pension Yojana",
            "ministry": "Ministry of Finance",
            "description": "Pension scheme for unorganized sector workers.",
            "eligibility_rules": "Any citizen between 18-40 years with a bank account.",
            "benefits": "Guaranteed minimum pension of Rs 1000-5000 per month after 60.",
            "min_age": 18,
            "max_age": 40, # STRICT UPPER LIMIT
            "max_income": None,
            "required_gender": None,
            "category": "Pension",
            "apply_url": "https://www.myscheme.gov.in/schemes/apy"
        },
        {
            "scheme_name": "Pradhan Mantri Shram Yogi Maandhan (PM-SYM)",
            "ministry": "Ministry of Labour",
            "description": "Voluntary and contributory pension scheme for unorganized workers.",
            "eligibility_rules": "Unorganized workers, entry age 18-40, monthly income <= Rs 15000.",
            "benefits": "Minimum assured pension of Rs 3000/month after 60.",
            "min_age": 18,
            "max_age": 40, # STRICT UPPER LIMIT
            "max_income": 180000, 
            "required_gender": None,
            "category": "Pension",
            "apply_url": "https://www.myscheme.gov.in/schemes/pm-sym"
        },
        {
            "scheme_name": "Old Age Pension (NSAP)",
            "ministry": "Ministry of Rural Development",
            "description": "Social assistance benefit to poor elderly.",
            "eligibility_rules": "60 years and above, BPL.",
            "benefits": "Monthly pension (varies by state approx Rs 200-1000).",
            "min_age": 60,
            "max_age": None,
            "max_income": 60000, 
            "required_gender": None,
            "category": "Pension",
            "apply_url": "https://www.myscheme.gov.in/schemes/ignoaps"
        },

    ]
    
    for item in schemes_data:
        scheme = models.Scheme(**item)
        db.add(scheme)
    
    db.commit()
    print(f"Successfully seeded {len(schemes_data)} schemes.")
    db.close()

if __name__ == "__main__":
    seed_schemes()
