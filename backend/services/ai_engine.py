import pickle
import os
import numpy as np
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../ml_models/risk_model.pkl')

class AIEngine:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.load_model()

    def load_model(self):
        try:
            if os.path.exists(MODEL_PATH):
                with open(MODEL_PATH, 'rb') as f:
                    artifacts = pickle.load(f)
                    self.model = artifacts['model']
                    self.encoders = artifacts['encoders']
                print("AI Model loaded successfully.")
            else:
                print(f"Warning: AI Model not found at {MODEL_PATH}. Using fallback mock logic.")
        except Exception as e:
            print(f"Error loading AI model: {e}")

    def predict_risk(self, profile_data: dict) -> float:
        """
        Predicts welfare risk score (0.0 to 1.0) using trained ML model.
        """
        if not self.model:
            return self._fallback_logic(profile_data)

        try:
            # Feature alignment with train_model.py: 
            # ['age', 'gender_enc', 'income', 'caste_enc', 'location_enc', 'education_enc', 'occupation_enc', 'state_enc']
            
            def safe_encode(encoder, value, default_idx=0):
                if value in encoder.classes_:
                    return encoder.transform([value])[0]
                return default_idx

            input_features = [
                profile_data.get('age', 30),
                safe_encode(self.encoders['gender'], profile_data.get('gender', 'Other')),
                profile_data.get('income', 50000),
                safe_encode(self.encoders['caste'], profile_data.get('community', 'General')),
                safe_encode(self.encoders['location'], profile_data.get('location_type', 'Urban')),
                safe_encode(self.encoders['education'], profile_data.get('education', 'Graduate')),
                safe_encode(self.encoders['occupation'], profile_data.get('occupation', 'Unemployed')),
                safe_encode(self.encoders['state'], profile_data.get('location_state', 'Delhi'))
            ]
            
            # The model predicts 0 (Low), 1 (Medium), 2 (High) need.
            # We convert this to a continuous scale for the UI gauge.
            prediction_class = self.model.predict([input_features])[0]
            
            # Basic mapping class -> score
            score_map = {0: 0.25, 1: 0.55, 2: 0.85}
            base_score = score_map.get(prediction_class, 0.5)
            
            # Add some slight variance based on income for smoothness
            income = profile_data.get('income', 50000)
            variance = (1 - (min(income, 1000000) / 1000000)) * 0.1
            
            return min(max(base_score + variance, 0.0), 1.0)
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return self._fallback_logic(profile_data)

    def _fallback_logic(self, profile_data):
        # ROI: Rule Based Fallback
        income = profile_data.get('income', 0)
        age = profile_data.get('age', 0)
        
        score = 0.2
        if income < 100000: score += 0.3
        if age > 60: score += 0.2
        if profile_data.get('disability_status'): score += 0.2
        if profile_data.get('location_type') == 'Rural': score += 0.1
        comm = profile_data.get('community', '')
        if comm and comm in ['SC', 'ST']: score += 0.1
        
        return min(max(score, 0.0), 1.0)

ai_engine = AIEngine()
