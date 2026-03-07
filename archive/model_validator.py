# ==============================================
# Phase 3 – Step 1: Scoring Engine
# ==============================================
import os
import pickle
import pandas as pd

# -------------------------------------------------
# 1️⃣ Load Model & Feature Columns
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # points to /ml
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODEL_DIR, "predictive_model.pkl")
FEATURE_PATH = os.path.join(MODEL_DIR, "feature_columns.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("❌ predictive_model.pkl not found")

if not os.path.exists(FEATURE_PATH):
    raise FileNotFoundError("❌ feature_columns.pkl not found")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(FEATURE_PATH, "rb") as f:
    feature_columns = pickle.load(f)

print("✅ Model and feature columns loaded successfully")


# -------------------------------------------------
# 2️⃣ Feature Preparation Function
# -------------------------------------------------
def prepare_features(input_df):
    df = input_df.copy()

    # Drop unwanted columns (same logic as Phase 2)
    drop_cols = ["worker_id", "job_id", "title", "description"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Remove target column if accidentally included
    if "final_rating" in df.columns:
        df = df.drop(columns=["final_rating"])

    # Apply encoding
    df = pd.get_dummies(df, drop_first=True)

    # Ensure all training columns exist
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # Ensure same column order
    df = df[feature_columns]

    return df


# -------------------------------------------------
# 3️⃣ Prediction Function
# -------------------------------------------------
def predict_score(worker_job_row: pd.DataFrame):
    processed = prepare_features(worker_job_row)
    prediction = model.predict(processed)
    return prediction[0]


# -------------------------------------------------
# 4️⃣ Example Test Run
# -------------------------------------------------
if __name__ == "__main__":

    sample_data = pd.DataFrame([{
        "skill_similarity": 0.85,
        "experience_bucket": 2,
        "avg_rating": 4.2,
        "distance_km": 5.0,
        "budget": 20000,
        "status": "completed",  # must match real dataset values
        "cluster_id": 1
    }])

    score = predict_score(sample_data)

    print(f"\n🎯 Predicted Performance Score: {round(score, 4)}")
# -------------------------------------------------
# 4️⃣ Ranking Function (Phase 3 - Step 2)
# -------------------------------------------------
def recommend_workers_for_job(job_id, top_n=5):
    """
    Finds and ranks workers for a specific job from the dataset.
    """
    # Define path to the processed data
    # BASE_DIR is /ml, so we go up to LabourNearMe, then down to data
    DATA_PATH = os.path.join(os.path.dirname(BASE_DIR), "data", "processed", "ml_ready_dataset.csv")

    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Dataset not found at {DATA_PATH}")
        return None

    df = pd.read_csv(DATA_PATH)

    # Filter rows belonging to this job ID
    job_df = df[df["job_id"] == job_id]

    if job_df.empty:
        print(f"⚠ No worker data found for Job ID: {job_id}")
        return None

    results = []
    for _, row in job_df.iterrows():
        worker_id = row["worker_id"]
        # Convert the row to a single-row DataFrame for the prediction function
        row_df = pd.DataFrame([row])
        score = predict_score(row_df)
        
        results.append({
            "worker_id": worker_id,
            "predicted_score": round(float(score), 2)
        })

    # Sort results: highest score first
    rankings = pd.DataFrame(results).sort_values(by="predicted_score", ascending=False)
    return rankings.head(top_n)


# -------------------------------------------------
# 5️⃣ Updated Test Run
# -------------------------------------------------
if __name__ == "__main__":
    # Test 1: Single Scoring
    sample_data = pd.DataFrame([{
        "skill_similarity": 0.85, "experience_bucket": 2, "avg_rating": 4.2,
        "distance_km": 5.0, "budget": 20000, "status": "completed", "cluster_id": 1
    }])
    score = predict_score(sample_data)
    print(f"\n🎯 Single Test Score: {round(score, 4)}")

    # Test 2: Full Ranking (Use one of the UUIDs from your dataset)
    test_job_id = "e7216864-f1da-449f-a3a6-7107359798bf" 
    print(f"\n🔍 Ranking workers for Job: {test_job_id}...")
    
    rankings = recommend_workers_for_job(test_job_id)
    if rankings is not None:
        print("\n🏆 Top Recommended Workers:")
        print(rankings.to_string(index=False))