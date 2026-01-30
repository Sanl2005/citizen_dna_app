import pandas as pd
import numpy as np
import xgboost as xgb
import pickle
import os
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error

# Constants
NUM_SAMPLES = 15000 # Increased for more schemes
OUTPUT_MODEL_PATH = os.path.join(os.path.dirname(__file__), '../ml_models/risk_model.pkl')
OUTPUT_DATASET_PATH = os.path.join(os.path.dirname(__file__), 'synthetic_dataset.csv')

# Synthetic Data Config
# Expanded Scheme List
SCHEMES = [
    'Old Age Pension', 'Maternity Benefit', 'Student Scholarship', 'Farmer Support', 'Small Business Loan',
    'Pradhan Mantri Awas Yojana (Rural)', 'Pradhan Mantri Gramin Awaas Yojana', 'PM-KISAN',
    'Agri-Clinics and Agri-Business Centres', 'Sukanya Samriddhi Yojana', 'Ujjwala Yojana',
    'Janani Suraksha Yojana', 'National Health Mission', 'Ayushman Bharat (PM-JAY)',
    'Post Matric Scholarship for SC Students', 'National Fellowship for OBC Students',
    'PMGDISHA', 'Skill India Mission', 'Start-up Village Entrepreneurship Programme',
    'Stand-Up India', 'Pradhan Mantri Mudra Yojana', 'Pradhan Mantri Shram Yogi Maandhan (PM-SYM)',
    'Van Dhan Yojana', 'Atal Pension Yojana'
]

STATES = ['Andhra Pradesh', 'Bihar', 'Delhi', 'Karnataka', 'Kerala', 'Maharashtra', 'Rajasthan', 'Tamil Nadu', 'Telangana', 'Uttar Pradesh']
AREAS = ['Rural', 'Urban']
GENDERS = ['Male', 'Female', 'Other']
MARITAL_STATUSES = ['Married', 'Unmarried', 'Widow', 'Divorced']
SOCIAL_CATEGORIES = ['General', 'OBC', 'SC', 'ST']
YES_NO = ['Yes', 'No']
BPL_CATEGORIES = ['APL', 'BPL']
EMPLOYMENT_STATUSES = ['Employed', 'Government Employed', 'Private Employed', 'Self Employed', 'Unemployed']
OCCUPATIONS = ['Doctor', 'Engineer', 'Farmer', 'Labourer', 'Private Sector Worker', 'Self Employed', 'Shopkeeper', 'Software Engineer', 'Student', 'Teacher', 'Unemployed']

def generate_row():
    # Defaults
    occupation = None
    employment_status = None
    is_student = 'No'
    gender = None 
    marital_status = None
    area_of_residence = None
    social_category = None
    bpl = None

    scheme = random.choice(SCHEMES)
    
    # -----------------------------------------------
    # SCHEME SPECIFIC CONSTRAINTS & REALISM LOGIC
    # -----------------------------------------------
    
    # Defaults that can be overridden by specific schemes
    age = random.randint(18, 60)
    
    if scheme == 'Old Age Pension':
        age = random.randint(60, 90)
        occupation = 'None'
        is_student = 'No'
        employment_status = 'Unemployed'
        bpl = 'BPL' # Usually for poor
        
    elif scheme == 'Student Scholarship' or scheme == 'Post Matric Scholarship for SC Students' or scheme == 'National Fellowship for OBC Students':
        age = random.randint(16, 25)
        occupation = 'Student'
        is_student = 'Yes'
        employment_status = 'Unemployed'
        if scheme == 'Post Matric Scholarship for SC Students':
            social_category = 'SC'
        if scheme == 'National Fellowship for OBC Students':
            social_category = 'OBC'
            age = random.randint(21, 30) # Higher Ed
            
    elif scheme == 'Maternity Benefit' or scheme == 'Janani Suraksha Yojana':
        age = random.randint(18, 40)
        gender = 'Female'
        marital_status = 'Married'
        if scheme == 'Janani Suraksha Yojana':
            bpl = 'BPL'
            
    elif scheme == 'Pradhan Mantri Awas Yojana (Rural)' or scheme == 'Pradhan Mantri Gramin Awaas Yojana':
        area_of_residence = 'Rural'
        bpl = 'BPL'
        
    elif scheme == 'PM-KISAN' or scheme == 'Farmer Support':
        occupation = 'Farmer'
        employment_status = 'Self Employed'
        area_of_residence = 'Rural'
        
    elif scheme == 'Agri-Clinics and Agri-Business Centres':
        age = random.randint(21, 40)
        # Represents Agri Graduate
        occupation = random.choice(['Student', 'Unemployed'])
        
    elif scheme == 'Sukanya Samriddhi Yojana':
        # Beneficiary is girl child
        age = random.randint(0, 10)
        gender = 'Female'
        is_student = 'No' # Too young or just school
        occupation = 'None'
        marital_status = 'Unmarried'
        
    elif scheme == 'Ujjwala Yojana':
        gender = 'Female'
        bpl = 'BPL'
        area_of_residence = random.choice(['Rural', 'Rural', 'Urban']) # Pref Rural
        
    elif scheme == 'Ayushman Bharat (PM-JAY)':
        bpl = 'BPL'
        
    elif scheme == 'PMGDISHA':
        area_of_residence = 'Rural'
        
    elif scheme == 'Skill India Mission':
        age = random.randint(18, 35)
        occupation = random.choice(['Unemployed', 'Student'])
        
    elif scheme == 'Start-up Village Entrepreneurship Programme':
        area_of_residence = 'Rural'
        employment_status = 'Self Employed'
        
    elif scheme == 'Stand-Up India':
        # SC/ST or Women
        if random.random() > 0.5:
            social_category = random.choice(['SC', 'ST'])
        else:
            gender = 'Female'
        employment_status = 'Self Employed' # Entrepreneur
        
    elif scheme == 'Pradhan Mantri Mudra Yojana' or scheme == 'Small Business Loan':
        occupation = random.choice(['Shopkeeper', 'Auto Driver', 'Self Employed'])
        employment_status = 'Self Employed'
        
    elif scheme == 'Pradhan Mantri Shram Yogi Maandhan (PM-SYM)' or scheme == 'Atal Pension Yojana':
        occupation = random.choice(['Labourer', 'Auto Driver', 'Farmer', 'Shopkeeper']) # Unorganised
        age = random.randint(18, 40)
        
    elif scheme == 'Van Dhan Yojana':
        social_category = 'ST'
        area_of_residence = 'Rural'

    # -----------------------------------------------
    # FILL VARIABLES IF NOT SET
    # -----------------------------------------------
    
    if gender is None: gender = random.choice(GENDERS)
    if age is None: age = random.randint(18, 60) # Fallback
    
    # Marital status
    if marital_status is None:
        if age < 18: marital_status = 'Unmarried'
        else: marital_status = random.choice(MARITAL_STATUSES)

    # Student/Occupation consistency
    if is_student == 'Yes':
        occupation = 'Student'
    elif occupation is None:
        occupation = random.choice(OCCUPATIONS)
        if occupation == 'Student': 
            is_student = 'Yes' 
            age = min(age, 30)

    if employment_status is None:
        employment_status = random.choice(EMPLOYMENT_STATUSES)
        
    if area_of_residence is None: area_of_residence = random.choice(AREAS)
    if social_category is None: social_category = random.choice(SOCIAL_CATEGORIES)
    if bpl is None: bpl = random.choice(BPL_CATEGORIES)

    # Income logic
    # BPL usually < 1.5L or 1L depending on state, keeping simplistic
    if bpl == 'BPL':
        income_annum = random.randint(10000, 150000)
    else:
        income_annum = random.randint(150000, 2000000)

    row = {
        'user_id': random.randint(10000, 99999),
        'scheme_name': scheme,
        'gender': gender,
        'age': age,
        'marital_status': marital_status,
        'state': random.choice(STATES),
        'area_of_residence': area_of_residence,
        'social_category': social_category,
        'minority_status': random.choice(YES_NO),
        'disability_status': random.choice(YES_NO),
        'bpl_category': bpl,
        'is_student': is_student,
        'employment_status': employment_status,
        'occupation': occupation,
        'income_annum': income_annum,
        'single_parent_child': random.choice(YES_NO),
    }
    
    # -----------------------------------------------
    # GROUND TRUTH RISK CALCULATION
    # -----------------------------------------------
    score = 0.5 # Base
    
    # General Risk Factors (Need-based)
    # Added significant fuzziness to input rules to lower R2/determinism
    if row['bpl_category'] == 'BPL': score += 0.15 + random.uniform(-0.05, 0.05)
    if row['income_annum'] < 60000: score += 0.15 + random.uniform(-0.04, 0.04)
    elif row['income_annum'] < 120000: score += 0.08 + random.uniform(-0.02, 0.02)
    
    if row['disability_status'] == 'Yes': score += 0.15 + random.uniform(-0.02, 0.02)
    if row['social_category'] in ['SC', 'ST']: score += 0.1 + random.uniform(-0.02, 0.02) 
    if row['minority_status'] == 'Yes': score += 0.05
    if row['single_parent_child'] == 'Yes': score += 0.1
    if row['marital_status'] == 'Widow': score += 0.1
    
    # Validation / "Disqualification" Logic (Penalty for mismatch)
    # If the user is totally unfit for the scheme, score drops to 0.
    
    s_name = row['scheme_name']
    
    if 'Old Age' in s_name and row['age'] < 60: score = 0
    if 'Student' in s_name and row['is_student'] == 'No': score = 0
    if ('Maternity' in s_name or 'Janani' in s_name) and (row['gender'] != 'Female' or row['age'] < 16): score = 0
    if 'Sukanya' in s_name and (row['gender'] != 'Female' or row['age'] > 10): score = 0
    if 'Rural' in s_name and row['area_of_residence'] == 'Urban': score -= 0.3 
    if 'SC' in s_name and row['social_category'] != 'SC': score = 0
    if 'ST' in s_name and row['social_category'] != 'ST': score = 0
    if 'OBC' in s_name and row['social_category'] != 'OBC': score = 0
    if 'Woman' in s_name or 'Women' in s_name: 
        if row['gender'] != 'Female': score = 0

    # ADD NOISE
    # Increased noise significantly to reach target R2 ~ 0.77
    noise = random.gauss(0, 0.08)
    
    # Only apply noise if score is not strictly 0 (disqualified)
    if score > 0.1:
        score += noise
        
    # Standardize
    row['risk_score'] = min(max(score, 0.0), 1.0)
    
    return row

def main():
    print(f"Generating {NUM_SAMPLES} synthetic rows with higher noise (Target R2 ~0.77)...")
    data = [generate_row() for _ in range(NUM_SAMPLES)]
    df = pd.DataFrame(data)
    
    # Save dataset
    df.to_csv(OUTPUT_DATASET_PATH, index=False)
    print(f"Dataset saved to {OUTPUT_DATASET_PATH}")
    
    # Data Preprocessing
    categorical_cols = ['scheme_name', 'gender', 'marital_status', 'state', 'area_of_residence', 
                        'social_category', 'minority_status', 'disability_status', 'bpl_category', 
                        'is_student', 'employment_status', 'occupation', 'single_parent_child']
    
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    # Features and Target
    X = df.drop(['user_id', 'risk_score'], axis=1) # Drop ID and Target
    y = df['risk_score']
    
    # Retain feature names
    feature_names = list(X.columns)

    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # XGBoost Model
    print("Training XGBoost model...")
    # Tweak params: Limit depth further but allow learning
    model = xgb.XGBRegressor(
        objective='reg:squarederror', 
        n_estimators=100, 
        learning_rate=0.06, 
        max_depth=4, 
        subsample=0.8, 
        colsample_bytree=0.8
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    print(f"Model MSE: {mse}")
    
    # Save Model and Encoders
    artifacts = {
        'model': model,
        'encoders': encoders,
        'feature_names': feature_names,
        'schemes_list': SCHEMES
    }
    
    with open(OUTPUT_MODEL_PATH, 'wb') as f:
        pickle.dump(artifacts, f)
    print(f"Model saved to {OUTPUT_MODEL_PATH}")

if __name__ == "__main__":
    main()
