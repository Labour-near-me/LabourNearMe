#this trains the lodaded model and prepares the features correctly.
import os
import pickle
import pandas as pd

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODEL_DIR, "predictive_model.pkl")
FEATURE_PATH = os.path.join(MODEL_DIR, "feature_columns.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(FEATURE_PATH, "rb") as f:
    feature_columns = pickle.load(f)

print("✅ Predictive model loaded")

# -------------------------------------------------
# FEATURE PREPARATION
# -------------------------------------------------

def prepare_features(df):

    df = df.copy()

    drop_cols = ["worker_id", "job_id", "title", "description"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")

    if "final_rating" in df.columns:
        df = df.drop(columns=["final_rating"])

    df = pd.get_dummies(df)

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]

    return df

# -------------------------------------------------
# SCORE PREDICTION
# -------------------------------------------------

def predict_score(row_df):

    features = prepare_features(row_df)

    prediction = model.predict(features)

    return float(prediction[0])