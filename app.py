from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Cardiovascular Risk & Vessel Stenosis Prediction API",
    version="3.0",
    description="Backend API serving leakage-free, pipeline-wrapped models for global CAD and vessel stenosis.",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    patient_id: Optional[str] = "N/A"
    Age: int = Field(..., ge=18, le=120)
    Sex: str  # "Male" or "Fmale"
    BMI: float = Field(..., ge=10.0, le=60.0)
    FBS: float = Field(..., ge=50, le=500)
    EF_TTE: float = Field(..., ge=10, le=80)
    HTN: int
    Current_Smoker: int
    Typical_Chest_Pain: int
    VHD: str  # "N", "mild", "Severe"

# Load the exact exported pipeline models from your Colab bundle
try:
    models = {
        "cath": joblib.load("cad_models_bundle/model_rf_cath.pkl"),
        "lad": joblib.load("cad_models_bundle/model_xgb_lad.pkl"),
        "lcx": joblib.load("cad_models_bundle/model_xgb_lcx.pkl"),
        "rca": joblib.load("cad_models_bundle/model_xgb_rca.pkl"),
    }
except Exception as e:
    models = {}
    print(f"Warning: Failed to load pipeline models: {e}")

@app.get("/")
def root():
    return {"status": "online", "message": "Cardiovascular Risk Pipeline API is running."}

@app.post("/predict")
def predict_cardiac_risk(patient_data: PatientData):
    if not models:
        raise HTTPException(
            status_code=500,
            detail="Pipeline models not loaded. Ensure 'cad_models_bundle (1)/' folder is present.",
        )

    try:
        # Reconstruct the exact 44 features expected by your trained pipelines, 
        # safely filling any pruned/dropped columns with standard baseline medians.
        feature_dict = {
            "Age": patient_data.Age,
            "Length": 165.0,
            "Sex": patient_data.Sex,
            "BMI": patient_data.BMI,
            "HTN": patient_data.HTN,
            "Current Smoker": patient_data.Current_Smoker,
            "EX-Smoker": 0,
            "FH": 0,
            "CRF": "N",
            "CVA": "N",
            "Airway disease": "N",
            "Thyroid Disease": "N",
            "CHF": "N",
            "DLP": "Y",
            "BP": 120.0,
            "PR": 75,
            "Edema": 0,
            "Weak Peripheral Pulse": "N",
            "Lung rales": "N",
            "Systolic Murmur": "N",
            "Diastolic Murmur": "N",
            "Typical Chest Pain": patient_data.Typical_Chest_Pain,
            "Dyspnea": "N",
            "Function Class": 0,
            "Atypical": "N",
            "Nonanginal": "N",
            "LowTH Ang": "N",
            "Q Wave": 0,
            "St Depression": 0,
            "Tinversion": 0,
            "LVH": "N",
            "Poor R Progression": "N",
            "BBB": "N",
            "FBS": patient_data.FBS,
            "CR": 0.9,
            "TG": 150,
            "LDL": 110,
            "HDL": 42.0,
            "BUN": 15,
            "ESR": 12,
            "HB": 13.5,
            "K": 4.2,
            "Na": 140,
            "WBC": 7500,
            "Lymph": 32,
            "PLT": 220,
            "EF-TTE": patient_data.EF_TTE,
            "VHD": patient_data.VHD,
        }

        input_df = pd.DataFrame([feature_dict])

        predictions = {}
        for target_name, pipeline in models.items():
            prob = float(pipeline.predict_proba(input_df)[0][1])
            is_high_risk = prob >= 0.5

            predictions[target_name] = {
                "risk_score": round(prob * 100, 1),
                "probability": round(prob, 4),
                "status": "STENOTIC (High Risk)" if is_high_risk else "NORMAL (Low Risk)",
                "color": "#ef4444" if is_high_risk else "#22c55e",
            }

        return {"patient_id": patient_data.patient_id, "results": predictions}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")