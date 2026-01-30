import pickle
import os
import numpy as np
import pandas as pd
import xgboost as xgb

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../ml_models/risk_model.pkl')

class AIEngine:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.feature_names = []
        self.load_model()

    def load_model(self):
        try:
            if os.path.exists(MODEL_PATH):
                with open(MODEL_PATH, 'rb') as f:
                    artifacts = pickle.load(f)
                    self.model = artifacts['model']
                    self.encoders = artifacts['encoders']
                    self.feature_names = artifacts.get('feature_names', [])
                print("AI Model loaded successfully.")
            else:
                print(f"Warning: AI Model not found at {MODEL_PATH}. Using fallback mock logic.")
        except Exception as e:
            print(f"Error loading AI model: {e}")

    def predict_risk(self, profile_data: dict) -> float:
        """
        Predicts welfare risk score (0.0 to 1.0) using trained XGBoost model.
        """
        if not self.model:
            return self._fallback_logic(profile_data)

        try:
            # Map Profile Data to Model Features
            age = profile_data.get('age', 30)
            gender = profile_data.get('gender', 'Male')
            occupation = profile_data.get('occupation', 'Unemployed')
            income = profile_data.get('income', 50000)
            
            # Smart Inference for Context-Dependent Fields
            # Determine the most applicable scheme context for risk evaluation
            scheme_name = 'Pradhan Mantri Mudra Yojana' # Default / Business Loan
            
            is_student_val = 'No'
            if 'Student' in occupation or (age < 25 and occupation == 'Unemployed'):
                is_student_val = 'Yes'

            # Logic Hierarchy
            if age >= 60:
                scheme_name = 'Old Age Pension'
            elif age <= 10 and gender == 'Female':
                scheme_name = 'Sukanya Samriddhi Yojana'
            elif 'Farmer' in occupation:
                scheme_name = 'PM-KISAN'
            elif is_student_val == 'Yes':
                if profile_data.get('community') == 'SC':
                    scheme_name = 'Post Matric Scholarship for SC Students'
                elif profile_data.get('community') == 'OBC':
                    scheme_name = 'National Fellowship for OBC Students'
                else:
                    scheme_name = 'Student Scholarship'
            elif gender == 'Female' and 18 <= age <= 40 and profile_data.get('marital_status') == 'Married':
                 # Pregnancy context usually assumed for these schemes if married/age fit
                scheme_name = 'Janani Suraksha Yojana' 
            elif profile_data.get('area_of_residence') == 'Rural' and bpl == 'BPL':
                scheme_name = 'Pradhan Mantri Awas Yojana (Rural)'
            elif occupation in ['Labourer']:
                scheme_name = 'Pradhan Mantri Shram Yogi Maandhan (PM-SYM)'
            elif occupation in ['Shopkeeper', 'Self Employed']:
                if gender == 'Female' or profile_data.get('community') in ['SC', 'ST']:
                    scheme_name = 'Stand-Up India'
                else:
                    scheme_name = 'Pradhan Mantri Mudra Yojana'
            
            # Derived fields
            is_student = profile_data.get('is_student', 'No')
            # Double check inference if explicit flag is somehow wrong but occupation is Student
            if is_student == 'No' and occupation == 'Student':
                is_student = 'Yes'
                
            marital_status = 'Unmarried' if age < 25 else 'Married' 

            bpl = profile_data.get('bpl_category', 'APL')
            if income < 150000: bpl = 'BPL'
            
            emp_status = profile_data.get('employment_status', 'Unemployed')
            # Fallback inference if missing
            if emp_status == 'Unemployed' and occupation != 'Unemployed':
                if occupation in ['Farmer', 'Shopkeeper', 'Self Employed']: emp_status = 'Self Employed'
                elif occupation in ['Doctor', 'Engineer', 'Software Engineer', 'Teacher', 'Private Sector Worker']: emp_status = 'Private Employed'
            
            raw_input = {
                'scheme_name': scheme_name,
                'gender': gender,
                'age': age,
                'marital_status': marital_status,
                'state': profile_data.get('location_state', 'Delhi'),
                'area_of_residence': profile_data.get('area_of_residence', 'Urban'),
                'social_category': profile_data.get('community', 'General'),
                'minority_status': 'No', 
                'disability_status': 'Yes' if profile_data.get('disability_status') else 'No',
                'bpl_category': bpl,
                'is_student': is_student,
                'employment_status': emp_status,
                'occupation': occupation,
                'income_annum': income,
                'single_parent_child': profile_data.get('single_parent_child', 'No')
            }

            # Prepare Input Vector
            input_vector = []
            features_order = self.feature_names if self.feature_names else [
               'scheme_name', 'gender', 'age', 'marital_status', 'state', 'area_of_residence', 
               'social_category', 'minority_status', 'disability_status', 'bpl_category', 
               'is_student', 'employment_status', 'occupation', 'income_annum', 'single_parent_child'
            ]
            
            for feature in features_order:
                value = raw_input.get(feature)
                
                # Check if this feature needs encoding
                if feature in self.encoders:
                    encoder = self.encoders[feature]
                    # Handle unseen labels by defaulting to the first class
                    if value not in encoder.classes_:
                        value = encoder.classes_[0] # Fallback
                    
                    encoded_value = encoder.transform([value])[0]
                    input_vector.append(encoded_value)
                else:
                    # Numeric features
                    input_vector.append(value)

            # Predict
            input_df = pd.DataFrame([input_vector], columns=features_order)
            prediction = self.model.predict(input_df)[0]
            
            return float(min(max(prediction, 0.0), 1.0))

        except Exception as e:
            print(f"Error in prediction: {e}")
            return self._fallback_logic(profile_data)

    def calculate_financial_risk(self, profile):
        """
        Calculates financial vulnerability score (0-1).
        High score = High financial need.
        """
        score = 0.1
        income = profile.get('income', 0)
        occ = (profile.get('occupation') or "").lower()
        emp_status = (profile.get('employment_status') or "").lower()
        family_size = profile.get('family_size', 1)
        
        # Income factors
        if income <= 0: score += 0.5
        elif income < 50000: score += 0.4
        elif income < 150000: score += 0.25
        elif income < 300000: score += 0.1
        
        # Employment factors
        if emp_status == 'unemployed' and 'student' not in occ:
             score += 0.2
        if 'laborer' in occ or 'worker' in occ or 'vendor' in occ:
             score += 0.15
        if 'farmer' in occ:
             score += 0.1
             
        # Dependency burden
        if family_size > 4: score += 0.1
        if profile.get('single_parent_child') == 'Yes': score += 0.15
        
        return min(max(score, 0.05), 0.99)

    def calculate_health_risk(self, profile):
        """
        Calculates health vulnerability score (0-1).
        High score = High likelihood of needing health support.
        """
        score = 0.1
        age = profile.get('age', 25)
        disability = profile.get('disability_status', False)
        occ = (profile.get('occupation') or "").lower()
        
        # Age factors
        if age > 70: score += 0.6
        elif age > 60: score += 0.4
        elif age > 50: score += 0.2
        elif age < 5: score += 0.3 # Infant vulnerability
        elif age < 18: score += 0.1 # General child
        
        # Physical factors
        if disability: score += 0.4
        
        # Occupational Health Risk
        if any(x in occ for x in ['construction', 'mining', 'driver', 'hazard', 'laborer', 'factory']):
            score += 0.2
            
        # Socio-economic link
        if profile.get('income', 100000) < 100000:
            score += 0.1 # Poverty correlates with health risks
            
        return min(max(score, 0.05), 0.99)

    def _fallback_logic(self, profile_data):
        # Return average of specific risks
        fin = self.calculate_financial_risk(profile_data)
        hlt = self.calculate_health_risk(profile_data)
        return (fin + hlt) / 2

ai_engine = AIEngine()
