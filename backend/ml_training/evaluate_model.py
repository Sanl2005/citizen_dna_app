import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate():
    # Paths
    BASE_DIR = os.path.dirname(__file__)
    DATA_PATH = os.path.join(BASE_DIR, 'synthetic_dataset.csv')
    MODEL_PATH = os.path.join(BASE_DIR, '../ml_models/risk_model.pkl')

    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}")
        return
    
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        return

    print(f"Loading data from {DATA_PATH}...")
    # 'None' is a valid string in our dataset (e.g. for Occupation), so we disable default NA handling for it
    df = pd.read_csv(DATA_PATH, na_values=[], keep_default_na=False)

    print(f"Loading model from {MODEL_PATH}...")
    with open(MODEL_PATH, 'rb') as f:
        artifacts = pickle.load(f)
    
    model = artifacts['model']
    encoders = artifacts['encoders']
    
    # Preprocessing using saved encoders to ensure consistency
    categorical_cols = ['scheme_name', 'gender', 'marital_status', 'state', 'area_of_residence', 
                        'social_category', 'minority_status', 'disability_status', 'bpl_category', 
                        'is_student', 'employment_status', 'occupation', 'single_parent_child']

    print("Transforming features...")
    for col in categorical_cols:
        if col in encoders:
            le = encoders[col]
            # Use apply to handle potentially unseen labels gracefully (though unlikely with same dataset)
            # mapping known classes to transform, else default to 0 or similar could be done, 
            # but for metric evaluation on the same dataset, direct transform is standard.
            df[col] = le.transform(df[col])
        else:
            print(f"Warning: No encoder found for {col}")

    X = df.drop(['user_id', 'risk_score'], axis=1)
    y = df['risk_score']

    # Reproduce the exact split used in training
    print("Splitting data (test_size=0.2, random_state=42)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Evaluating on {len(X_test)} test samples...")
    preds = model.predict(X_test)

    # Metrics Calculation
    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    # Output Report
    print("\n" + "="*40)
    print("   XGBOOST MODEL PERFORMANCE REPORT")
    print("="*40)
    print(f"R-Squared (R²) Score : {r2:.5f}")
    print(f" - Interpreted as: The model explains {r2*100:.2f}% of the variance in risk scores.")
    print("-" * 40)
    print(f"RMSE (Root Mean Sq Error) : {rmse:.5f}")
    print(f"MAE (Mean Absolute Error) : {mae:.5f}")
    print(f"MSE (Mean Squared Error)  : {mse:.5f}")
    print("="*40)
    
    # Feature Importance
    print("\n" + "="*40)
    print("   FEATURE IMPORTANCE ANALYSIS")
    print("="*40)
    
    # Get importance (Gain is usually the default and most relevant for 'weight' interpretation in tree context, 
    # but feature_importances_ property gives Gini importance/Gain)
    importances = model.feature_importances_
    features = X.columns
    
    importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    
    for _, row in importance_df.iterrows():
        print(f"{row['Feature']:<25} : {row['Importance']:.4f} ({row['Importance']*100:.1f}%)")

    # Class Imbalance Check
    print("\n" + "="*40)
    print("   DATASET IMBALANCE CHECK")
    print("="*40)
    
    # Check Scheme Distribution
    print("Scheme Distribution:")
    scheme_counts = df['scheme_name'].value_counts(normalize=True) * 100
    # Mapping back to names if possible, but we transformed df inplace earlier. 
    # Let's reload concise raw data for readability or just use the indices if we must.
    # To keep it simple, we reload the raw CSV for accurate counts of labels.
    df_raw = pd.read_csv(DATA_PATH, na_values=[], keep_default_na=False)
    
    scheme_counts = df_raw['scheme_name'].value_counts()
    total_samples = len(df_raw)
    
    # Print top 10 and bottom 5 to check disparity
    print(f"Total Samples: {total_samples}")
    print("-" * 40)
    print(f"{'Scheme Name':<45} | {'Count':<6} | {'%':<5}")
    print("-" * 40)
    for scheme, count in scheme_counts.items():
        print(f"{scheme:<45} | {count:<6} | {count/total_samples*100:.1f}%")
        
    print("-" * 40)
    print("Social Category Distribution:")
    cat_counts = df_raw['social_category'].value_counts()
    for cat, count in cat_counts.items():
        print(f"{cat:<15} | {count:<6} | {count/total_samples*100:.1f}%")

    print("-" * 40)
    
    # Sample Comparison
    print("\nSample Predictions vs Ground Truth (First 5):")
    print(f"{'Actual':<10} | {'Predicted':<10} | {'Diff':<10}")
    print("-" * 34)
    for actual, pred in zip(y_test[:5].values, preds[:5]):
        print(f"{actual:<10.4f} | {pred:<10.4f} | {abs(actual-pred):<10.4f}")
    print("-" * 34)

if __name__ == "__main__":
    evaluate()
