from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os

from train import train_model
from predict import predict_eligibility

# --- Initialize FastAPI app ---
app = FastAPI(
    title="NGO Beneficiary Eligibility Analyzer",
    description="AI-powered API to determine NGO beneficiary eligibility",
    version="1.0.0"
)

# --- Load dataset helper ---
def load_dataset():
    if not os.path.exists("data/beneficiaries.csv"):
        raise HTTPException(status_code=404, detail="Dataset not found. Run dataset.py first.")
    return pd.read_csv("data/beneficiaries.csv")

# ============================================================
# PYDANTIC MODELS
# These define what data each endpoint expects to receive
# ============================================================

class Beneficiary(BaseModel):
    applicant_name:    str
    age:               int
    family_income:     int
    family_members:    int
    employment_status: str
    education_level:   str
    disability_status: str
    eligibility_status: str = None  # Optional, can be blank for new records

class PredictRequest(BaseModel):
    age:               int
    family_income:     int
    family_members:    int
    employment_status: str
    education_level:   str
    disability_status: str

# ============================================================
# BASIC ROUTES
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to NGO Beneficiary Eligibility Analyzer API!",
        "docs":    "Visit /docs to see all endpoints"
    }

# ============================================================
# BENEFICIARY CRUD ENDPOINTS
# ============================================================

# GET all beneficiaries
@app.get("/beneficiaries")
def get_beneficiaries():
    df = load_dataset()
    return df.to_dict(orient="records")

# GET a single beneficiary by ID (row index)
@app.get("/beneficiaries/{id}")
def get_beneficiary(id: int):
    df = load_dataset()
    if id < 0 or id >= len(df):
        raise HTTPException(status_code=404, detail=f"Record {id} not found")
    return df.iloc[id].to_dict()

# POST - Add a new beneficiary
@app.post("/beneficiaries")
def create_beneficiary(beneficiary: Beneficiary):
    df = load_dataset()
    new_row = pd.DataFrame([beneficiary.dict()])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("data/beneficiaries.csv", index=False)
    return {"message": "Beneficiary added successfully", "id": len(df) - 1}

# PUT - Update an existing beneficiary
@app.put("/beneficiaries/{id}")
def update_beneficiary(id: int, beneficiary: Beneficiary):
    df = load_dataset()
    if id < 0 or id >= len(df):
        raise HTTPException(status_code=404, detail=f"Record {id} not found")
    df.iloc[id] = beneficiary.dict()
    df.to_csv("data/beneficiaries.csv", index=False)
    return {"message": f"Beneficiary {id} updated successfully"}

# DELETE - Remove a beneficiary
@app.delete("/beneficiaries/{id}")
def delete_beneficiary(id: int):
    df = load_dataset()
    if id < 0 or id >= len(df):
        raise HTTPException(status_code=404, detail=f"Record {id} not found")
    df = df.drop(index=id).reset_index(drop=True)
    df.to_csv("data/beneficiaries.csv", index=False)
    return {"message": f"Beneficiary {id} deleted successfully"}

# ============================================================
# ML ENDPOINTS
# ============================================================

# POST - Train the model
@app.post("/train")
def train():
    try:
        model, X_test, y_test, name, accuracy = train_model()
        return {
            "message":  "Model trained successfully!",
            "model":    name,
            "accuracy": f"{accuracy * 100:.2f}%"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST - Predict eligibility
@app.post("/predict")
def predict(request: PredictRequest):
    try:
        prediction, confidence = predict_eligibility(
            age=               request.age,
            family_income=     request.family_income,
            family_members=    request.family_members,
            employment_status= request.employment_status,
            education_level=   request.education_level,
            disability_status= request.disability_status
        )
        return {
            "prediction": prediction,
            "confidence": round(confidence, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET - Analytics summary
@app.get("/analytics")
def analytics():
    df = load_dataset()
    return {
        "total_applicants":     len(df),
        "eligible_count":       int((df["eligibility_status"] == "Eligible").sum()),
        "not_eligible_count":   int((df["eligibility_status"] == "Not Eligible").sum()),
        "average_income":       round(df["family_income"].mean(), 2)
    }