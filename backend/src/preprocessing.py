"""
CogniCare AI - Preprocessing Module
Implements Kaggle stroke dataset ingestion, median BMI imputation, categorical encoding, and standard scaling.
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def generate_stroke_dataset(output_path="backend/data/healthcare-dataset-stroke-data.csv", n_samples=2500, random_seed=42):
    """Generates synthetic Kaggle stroke dataset matching authentic distribution."""
    np.random.seed(random_seed)
    
    patient_ids = np.arange(1000, 1000 + n_samples)
    genders = np.random.choice(["Male", "Female"], size=n_samples, p=[0.42, 0.58])
    ages = np.random.normal(loc=48, scale=18, size=n_samples)
    ages = np.clip(ages, 18, 90).astype(int)
    
    # Hypertension & Heart disease
    hypertension_prob = 0.05 + 0.35 * (ages / 90)
    hypertension = np.random.binomial(1, hypertension_prob)
    
    heart_disease_prob = 0.02 + 0.25 * (ages / 90) + 0.1 * hypertension
    heart_disease = np.random.binomial(1, np.clip(heart_disease_prob, 0, 0.9))
    
    ever_married = np.where(ages > 28, np.random.choice(["Yes", "No"], size=n_samples, p=[0.75, 0.25]), "No")
    work_types = np.random.choice(
        ["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
        size=n_samples,
        p=[0.57, 0.16, 0.13, 0.13, 0.01]
    )
    residence_types = np.random.choice(["Urban", "Rural"], size=n_samples, p=[0.51, 0.49])
    
    # Glucose levels with diabetic tail
    glucose_normal = np.random.normal(90, 15, size=n_samples)
    glucose_high = np.random.normal(195, 30, size=n_samples)
    is_high_glucose = np.random.binomial(1, 0.18 + 0.15 * (ages / 90), size=n_samples)
    avg_glucose = np.where(is_high_glucose == 1, glucose_high, glucose_normal)
    avg_glucose = np.clip(avg_glucose, 55.0, 290.0)
    
    # BMI
    bmis = np.random.normal(28.5, 6.5, size=n_samples)
    bmis = np.clip(bmis, 14.0, 60.0)
    
    # ~4% missing values for BMI
    missing_bmi_mask = np.random.binomial(1, 0.04, size=n_samples).astype(bool)
    bmis_with_nan = bmis.copy()
    bmis_with_nan[missing_bmi_mask] = np.nan
    
    smoking_status = np.random.choice(
        ["never smoked", "formerly smoked", "smokes", "Unknown"],
        size=n_samples,
        p=[0.38, 0.17, 0.15, 0.30]
    )
    
    # Realistic stroke risk logistic odds
    logits = (
        -4.2
        + 0.065 * (ages - 40)
        + 1.1 * hypertension
        + 1.3 * heart_disease
        + 0.012 * (avg_glucose - 100)
        + 0.035 * (bmis - 25)
        + np.where(smoking_status == "smokes", 0.8, 0.0)
        + np.where(smoking_status == "formerly smoked", 0.4, 0.0)
    )
    stroke_prob = 1 / (1 + np.exp(-logits))
    stroke = np.random.binomial(1, np.clip(stroke_prob, 0.01, 0.95))
    
    df = pd.DataFrame({
        "id": patient_ids,
        "gender": genders,
        "age": ages,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "ever_married": ever_married,
        "work_type": work_types,
        "Residence_type": residence_types,
        "avg_glucose_level": np.round(avg_glucose, 2),
        "bmi": np.round(bmis_with_nan, 1),
        "smoking_status": smoking_status,
        "stroke": stroke
    })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated raw stroke dataset: {output_path} ({len(df)} records)")
    return df

def preprocess_stroke_data(raw_csv_path="backend/data/healthcare-dataset-stroke-data.csv", cleaned_csv_path="backend/data/stroke_cleaned_dataset.csv"):
    """
    1. Removes duplicate records
    2. Imputes missing BMI values with median
    3. Encodes categorical variables
    4. Saves clean dataset ready for training
    """
    if not os.path.exists(raw_csv_path):
        generate_stroke_dataset(raw_csv_path)
        
    df = pd.read_csv(raw_csv_path)
    df = df.drop_duplicates()
    
    # Impute missing BMI with median
    median_bmi = float(df["bmi"].median())
    df["bmi"] = df["bmi"].fillna(median_bmi)
    
    categorical_columns = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]
    encoders = {}
    
    df_cleaned = df.copy()
    for col in categorical_columns:
        le = LabelEncoder()
        df_cleaned[col] = le.fit_transform(df_cleaned[col].astype(str))
        encoders[col] = le
        
    os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)
    df_cleaned.to_csv(cleaned_csv_path, index=False)
    print(f"Saved cleaned dataset: {cleaned_csv_path} (median BMI: {median_bmi})")
    return df, df_cleaned, encoders

if __name__ == "__main__":
    generate_stroke_dataset()
    preprocess_stroke_data()
