from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import joblib
import uuid
import pandas as pd
import os
from datetime import datetime
import json
import yaml

# ----------------------------
# Load Config
# ----------------------------

CONFIG_PATH = "src/config/config.yaml"

if not os.path.exists(CONFIG_PATH):
    raise Exception("Config file not found")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

LOG_FILE = config["logs"]["prediction_log_file"]

# Ensure logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


# ----------------------------
# Initialize App
# ----------------------------

app = FastAPI(title="ML Model API", version="1.0")


# ----------------------------
# Load Model (Versioned)
# ----------------------------

MODEL_PATH = config["model"]["path"]

if not os.path.exists(MODEL_PATH):
    raise Exception(f"Model not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

print(f"Model loaded from {MODEL_PATH}")


# ----------------------------
# Input Schema (Validation)
# ----------------------------

class PredictionInput(BaseModel):
    Runtime: float = Field(..., gt=0)
    Meta_score: float
    No_of_Votes: float
    Gross: float
    movie_age: float


# ----------------------------
# Initialize Log File
# ----------------------------

if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=[
        "request_id", "timestamp", "input", "prediction", "probability"
    ]).to_csv(LOG_FILE, index=False)


# ----------------------------
# Health Check
# ----------------------------

@app.get("/")
def home():
    return {
        "status": "API is running",
        "model_path": MODEL_PATH
    }


# ----------------------------
# Prediction Endpoint
# ----------------------------

@app.post("/predict")
async def predict(data: PredictionInput, request: Request):

    request_id = str(uuid.uuid4())

    try:
        input_dict = data.dict()

        df = pd.DataFrame([input_dict])

        prediction = model.predict(df)[0]

        # Probabilities (if available)
        if hasattr(model, "predict_proba"):
            prob = float(model.predict_proba(df)[0][1])
        else:
            prob = None

        # ----------------------------
        # Logging
        # ----------------------------

        log_entry = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "input": json.dumps(input_dict),
            "prediction": int(prediction),
            "probability": prob
        }

        pd.DataFrame([log_entry]).to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )

        return {
            "request_id": request_id,
            "prediction": int(prediction),
            "probability": prob
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))