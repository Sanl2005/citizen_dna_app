import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Create synthetic dataset
def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    
    data = {
        'age': np.random.randint(18, 90, n_samples),
        'income': np.random.randint(0, 500000, n_samples), # Annual income
        'family_size': np.random.randint(1, 10, n_samples),
        'disability_status': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
        'education_level': np.random.choice(['None', 'Primary', 'Secondary', 'Graduate'], n_samples),
        'occupation_type': np.random.choice(['Unemployed', 'Farmer', 'Laborer', 'Salaried', 'Business'], n_samples),
        'location_type': np.random.choice(['Rural', 'Urban'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate target variable (Risk Score: 0 to 1)
    # Logic: Lower income, higher age, disability, larger family -> Higher Risk
    
    risk_score = (
        (1 - (df['income'] / 500000)) * 0.4 + 
        (df['age'] / 90) * 0.2 +
        df['disability_status'] * 0.2 +
        (df['family_size'] / 10) * 0.2
    )
    
    # Add some noise
    risk_score += np.random.normal(0, 0.05, n_samples)
    risk_score = np.clip(risk_score, 0, 1)
    
    df['risk_score'] = risk_score
    
    return df

def train_model():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    # Preprocessing
    le_education = LabelEncoder()
    le_occupation = LabelEncoder()
    le_location = LabelEncoder()
    
    df['education_encoded'] = le_education.fit_transform(df['education_level'])
    df['occupation_encoded'] = le_occupation.fit_transform(df['occupation_type'])
    df['location_encoded'] = le_location.fit_transform(df['location_type'])
    
    X = df[['age', 'income', 'family_size', 'disability_status', 'education_encoded', 'occupation_encoded', 'location_encoded']]
    y = df['risk_score']
    
    print("Training Random Forest model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print(f"Model Score (R2): {model.score(X_test, y_test)}")
    
    # Save artifacts
    artifacts = {
        'model': model,
        'encoders': {
            'education': le_education,
            'occupation': le_occupation,
            'location': le_location
        }
    }
    
    output_path = os.path.join(os.path.dirname(__file__), '../ml_models/risk_model.pkl')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump(artifacts, f)
        
    print(f"Model saved to {output_path}")

if __name__ == "__main__":
    train_model()
