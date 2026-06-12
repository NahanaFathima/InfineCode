import joblib
import numpy as np
import pandas as pd

def predict_eligibility(age, family_income, family_members, 
                        employment_status, education_level, disability_status):
    """
    Predict eligibility for a new applicant.
    
    Parameters:
        age               : int   (e.g. 25)
        family_income     : int   (e.g. 120000)
        family_members    : int   (e.g. 4)
        employment_status : str   (e.g. "Unemployed")
        education_level   : str   (e.g. "Undergraduate")
        disability_status : str   (e.g. "No")
    
    Returns:
        prediction  : str   ("Eligible" or "Not Eligible")
        confidence  : float (e.g. 0.89)
    """

    # --- Step 1: Load the saved model and encoders ---
    model    = joblib.load("model/best_model.pkl")
    encoders = joblib.load("model/encoders.pkl")

    # --- Step 2: Encode the text inputs using saved encoders ---
    # We must use the SAME encoder that was used during training
    emp_encoded  = encoders["employment_status"].transform([employment_status])[0]
    edu_encoded  = encoders["education_level"].transform([education_level])[0]
    dis_encoded  = encoders["disability_status"].transform([disability_status])[0]

    # --- Step 3: Create input array in the same column order as training ---
    input_data = pd.DataFrame([{
        "age":               age,
        "family_income":     family_income,
        "family_members":    family_members,
        "employment_status": emp_encoded,
        "education_level":   edu_encoded,
        "disability_status": dis_encoded
    }])

    # --- Step 4: Make prediction ---
    prediction_encoded = model.predict(input_data)[0]

    # --- Step 5: Get confidence score ---
    # predict_proba returns probability for each class [Eligible, Not Eligible]
    probabilities = model.predict_proba(input_data)[0]
    confidence    = max(probabilities)  # Highest probability = confidence

    # --- Step 6: Decode prediction back to text ---
    prediction = encoders["eligibility_status"].inverse_transform([prediction_encoded])[0]

    return prediction, confidence


# --- Run if this file is executed directly ---
if __name__ == "__main__":
    print("=" * 40)
    print("   NGO BENEFICIARY ELIGIBILITY CHECK")
    print("=" * 40)

    # Test Case 1: Low income, unemployed
    prediction, confidence = predict_eligibility(
        age=22,
        family_income=120000,
        family_members=5,
        employment_status="Unemployed",
        education_level="Undergraduate",
        disability_status="No"
    )
    print(f"\nTest Case 1 (Low income + Unemployed):")
    print(f"  Prediction : {prediction}")
    print(f"  Confidence : {confidence * 100:.2f}%")

    # Test Case 2: High income, employed
    prediction, confidence = predict_eligibility(
        age=35,
        family_income=450000,
        family_members=3,
        employment_status="Employed",
        education_level="Postgraduate",
        disability_status="No"
    )
    print(f"\nTest Case 2 (High income + Employed):")
    print(f"  Prediction : {prediction}")
    print(f"  Confidence : {confidence * 100:.2f}%")

    # Test Case 3: High income but disabled
    prediction, confidence = predict_eligibility(
        age=40,
        family_income=400000,
        family_members=2,
        employment_status="Employed",
        education_level="Postgraduate",
        disability_status="Yes"
    )
    print(f"\nTest Case 3 (High income but Disabled):")
    print(f"  Prediction : {prediction}")
    print(f"  Confidence : {confidence * 100:.2f}%")