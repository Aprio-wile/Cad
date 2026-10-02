from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
from pydantic import BaseModel, Field

from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Cardiovascular Risk & Vessel Stenosis Prediction API",
    version="1.0",
    description="Backend API serving XGBoost predictions for overall CAD risk and coronary vessel stenosis (LAD, LCX, RCA).",
)

# Mount the static folder so the frontend can access the 3D model
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS for local frontend communication (Streamlit / React / Three.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Input validation schema for incoming patient payload
class PatientData(BaseModel):
    patient_id: Optional[str] = "N/A"
    Age: int = Field(..., ge=18, le=120, example=58)
    Sex: str = Field(..., example="Male")  # "Male" or "Female"
    BMI: float = Field(..., ge=10.0, le=60.0, example=28.5)
    Systolic_BP: float = Field(..., ge=70, le=250, example=130.0)
    FBS: float = Field(..., ge=50, le=500, example=110.0)
    EF_TTE: float = Field(..., ge=10, le=80, example=50.0)
    HTN: int = Field(..., description="1 if Hypertension present, 0 otherwise", example=1)
    DM: int = Field(..., description="1 if Diabetes Mellitus present, 0 otherwise", example=0)
    Current_Smoker: int = Field(..., description="1 if Smoker, 0 otherwise", example=0)
    Typical_Chest_Pain: int = Field(..., description="1 if present, 0 otherwise", example=1)
    VHD: str = Field(..., description="Valvular Heart Disease: N, mild, or Severe", example="N")


# Load trained XGBoost models at startup
try:
    models = {
        "cath": joblib.load("model_cath.pkl"),
        "lad": joblib.load("model_xgb_lad.pkl"),
        "lcx": joblib.load("model_xgb_lcx.pkl"),
        "rca": joblib.load("model_xgb_rca.pkl"),
    }
except Exception as e:
    models = {}
    print(f"Warning: Failed to load model .pkl files: {e}")


@app.get("/")
def root():
    return {"status": "online", "message": "Cardiovascular Risk Prediction API is running."}


@app.post("/predict")
def predict_cardiac_risk(patient_data: PatientData):
    """Accepts patient clinical parameters and returns probabilities and status for CAD, LAD, LCX, and RCA."""
    if not models:
        raise HTTPException(
            status_code=500,
            detail="Model files are not loaded on the server. Ensure .pkl files exist in the server directory.",
        )

    try:
        # Reconstruct the full baseline feature vector required by trained XGBoost models
        full_feature_dict = {
            "Age": patient_data.Age,
            "Weight": 70,
            "Length": 165,
            "Sex": patient_data.Sex,
            "BMI": patient_data.BMI,
            "DM": patient_data.DM,
            "HTN": patient_data.HTN,
            "Current Smoker": patient_data.Current_Smoker,
            "EX-Smoker": 0,
            "FH": 0,
            "Obesity": "Y" if patient_data.BMI >= 30 else "N",
            "CRF": "N",
            "CVA": "N",
            "Airway disease": "N",
            "Thyroid Disease": "N",
            "CHF": "N",
            "DLP": "Y",
            "BP": patient_data.Systolic_BP,
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
            "St Elevation": 0,
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
            "Neut": 60,
            "PLT": 220,
            "EF-TTE": patient_data.EF_TTE,
            "Region RWMA": 0,
            "VHD": patient_data.VHD,
        }

        input_df = pd.DataFrame([full_feature_dict])

        predictions = {}
        for target_name, model in models.items():
            prob = float(model.predict_proba(input_df)[0][1])
            is_high_risk = prob >= 0.5

            predictions[target_name] = {
                "risk_score": round(prob * 100, 1),
                "probability": round(prob, 4),
                "status": "STENOTIC (High Risk)" if is_high_risk else "NORMAL (Low Risk)",
                "color": "#ef4444" if is_high_risk else "#22c55e",  # Red vs Green
            }

        return {
            "patient_id": patient_data.patient_id,
            "results": predictions,
        }

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error calculating model predictions: {str(e)}"
        )