import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('citizen_large_dataset.csv')

# Preprocessing
# We want to predict if someone is "High Risk" (needs help) based on their features
# Or more simply, let's train it to predict the 'eligible_scheme' category
# For the purpose of the 'Risk Score', we'll create a synthetic risk label
# Low income + High age + Rural + Disability = Higher Risk

le_gender = LabelEncoder()
le_caste = LabelEncoder()
le_loc = LabelEncoder()
le_edu = LabelEncoder()
le_occ = LabelEncoder()
le_state = LabelEncoder()

df['gender_enc'] = le_gender.fit_transform(df['gender'])
df['caste_enc'] = le_caste.fit_transform(df['caste'])
df['location_enc'] = le_loc.fit_transform(df['location_type'])
df['education_enc'] = le_edu.fit_transform(df['education'])
df['occupation_enc'] = le_occ.fit_transform(df['occupation'])
df['state_enc'] = le_state.fit_transform(df['state'])

# Synthetic Risk Label (for the demo's Risk Score)
# normalized income (higher income = lower risk)
max_inc = df['income'].max()
inc_risk = 1 - (df['income'] / max_inc)
# age risk (older = higher risk)
age_risk = df['age'] / 100
# Combine
df['risk_score'] = (inc_risk * 0.6 + age_risk * 0.4)

# Features
X = df[['age', 'gender_enc', 'income', 'caste_enc', 'location_enc', 'education_enc', 'occupation_enc', 'state_enc']]
y = df['risk_score'] # For regression

# Let's actually train a classifier for "Welfare Need Level" (Low, Medium, High)
df['need_level'] = pd.qcut(df['risk_score'], 3, labels=[0, 1, 2]) # 0=Low, 1=Med, 2=High
y_class = df['need_level']

X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save artifacts
artifacts = {
    'model': model,
    'encoders': {
        'gender': le_gender,
        'caste': le_caste,
        'location': le_loc,
        'education': le_edu,
        'occupation': le_occ,
        'state': le_state
    }
}

os.makedirs('backend/ml_models', exist_ok=True)
with open('backend/ml_models/risk_model.pkl', 'wb') as f:
    pickle.dump(artifacts, f)

print("AI Model trained and saved successfully based on citizen dataset.")
