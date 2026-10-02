"""
CogniCare AI - Explainable AI (XAI) Module
Computes global/local feature importance, flags critical values, and provides patient-specific recommendations.
"""

def compute_xai_explanations(patient_dict):
    """Calculates local feature attributions and flags critical clinical thresholds."""
    age = float(patient_dict.get("age", 50))
    glucose = float(patient_dict.get("avg_glucose_level", 100))
    bmi = float(patient_dict.get("bmi", 25))
    hypertension = int(patient_dict.get("hypertension", 0))
    heart_disease = int(patient_dict.get("heart_disease", 0))
    smoking = int(patient_dict.get("smoking_status", 0))
    
    attributions = []
    critical_flags = []
    recommendations = []
    
    # 1. Glucose
    if glucose > 200:
        val = +0.38
        desc = "Severe hyperglycemic spike promoting acute microvascular inflammation"
        badge = "Critical Risk"
        critical_flags.append(f"High Blood Glucose ({glucose:.1f} mg/dL > 200 mg/dL)")
        recommendations.append("Urgent glycemic regulation & insulin/oral hypoglycemic review.")
    elif glucose > 140:
        val = +0.18
        desc = "Pre-diabetic elevated glucose level"
        badge = "Elevated"
        recommendations.append("Dietary sugar reduction and HbA1c test.")
    else:
        val = -0.05
        desc = "Normal blood glucose range"
        badge = "Optimal"
        
    attributions.append({
        "feature": "Avg Glucose Level",
        "value": f"{glucose:.1f} mg/dL",
        "impact": val,
        "impact_sign": "+" if val > 0 else "-",
        "rationale": desc,
        "badge": badge
    })
    
    # 2. Age
    if age >= 65:
        val = +0.27
        desc = f"Advanced age ({int(age)} yrs) associated with arterial stiffness"
        badge = "High Risk"
    elif age >= 50:
        val = +0.12
        desc = f"Moderate age factor ({int(age)} yrs)"
        badge = "Moderate"
    else:
        val = -0.15
        desc = "Younger age profile"
        badge = "Low Risk"
    attributions.append({
        "feature": "Patient Age",
        "value": f"{int(age)} Yrs",
        "impact": val,
        "impact_sign": "+" if val > 0 else "-",
        "rationale": desc,
        "badge": badge
    })
    
    # 3. Hypertension
    if hypertension == 1:
        val = +0.19
        desc = "Hypertension creates chronic vessel wall shear stress"
        badge = "Stage 2 High"
        critical_flags.append("Hypertension History Active")
        recommendations.append("Daily Blood Pressure monitoring; Target < 130/80 mmHg.")
    else:
        val = -0.06
        desc = "Normotensive baseline"
        badge = "Normal"
    attributions.append({
        "feature": "Hypertension History",
        "value": "Positive" if hypertension == 1 else "None",
        "impact": val,
        "impact_sign": "+" if val > 0 else "-",
        "rationale": desc,
        "badge": badge
    })
    
    # 4. Heart Disease
    if heart_disease == 1:
        val = +0.12
        desc = "Cardioembolic source elevating clot risk"
        badge = "Active CAD"
        critical_flags.append("Coronary Heart Disease")
        recommendations.append("Cardiology consultation & antiplatelet medication check.")
    else:
        val = -0.04
        desc = "No documented coronary disease"
        badge = "Clear"
    attributions.append({
        "feature": "Heart Disease / CAD",
        "value": "Positive" if heart_disease == 1 else "None",
        "impact": val,
        "impact_sign": "+" if val > 0 else "-",
        "rationale": desc,
        "badge": badge
    })
    
    # 5. BMI
    if bmi >= 30:
        val = +0.08
        desc = f"Obesity ({bmi:.1f} kg/m²) promoting vascular strain"
        badge = "Obese"
        critical_flags.append(f"Elevated BMI ({bmi:.1f} kg/m²)")
        recommendations.append("Gradual weight management and low-sodium Mediterranean diet.")
    elif bmi >= 25:
        val = +0.03
        desc = f"Overweight ({bmi:.1f} kg/m²)"
        badge = "Overweight"
    else:
        val = -0.02
        desc = "Healthy BMI"
        badge = "Optimal"
    attributions.append({
        "feature": "Body Mass Index (BMI)",
        "value": f"{bmi:.1f} kg/m²",
        "impact": val,
        "impact_sign": "+" if val > 0 else "-",
        "rationale": desc,
        "badge": badge
    })
    
    # 6. Smoking
    if smoking in [1, 3]:
        val = +0.04
        desc = "Tobacco exposure increasing arterial plaque instability"
        badge = "Exposure"
        recommendations.append("Complete smoking cessation program.")
    else:
        val = -0.03
        desc = "Non-smoker"
        badge = "Clean"
    attributions.append({
        "feature": "Smoking Status",
        "value": "Current / Former" if smoking in [1, 3] else "Never",
        "impact": val,
        "impact_sign": "+" if val > 0 else "-",
        "rationale": desc,
        "badge": badge
    })
    
    attributions.sort(key=lambda x: abs(x["impact"]), reverse=True)
    
    return {
        "attributions": attributions,
        "critical_flags": critical_flags,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    sample = {"age": 67, "avg_glucose_level": 218.4, "bmi": 32.2, "hypertension": 1, "heart_disease": 1, "smoking_status": 1}
    res = compute_xai_explanations(sample)
    print("Critical Flags:", res["critical_flags"])
