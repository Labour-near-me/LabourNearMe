import os
import ast
import numpy as np
import pandas as pd
import pickle
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity

# ================= CONFIG =================
SIMILARITY_THRESHOLD = 0.01
MAX_DISTANCE_KM = 50

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

# ================= MODEL =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "predictive_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "models", "feature_columns.pkl")

MODEL = pickle.load(open(MODEL_PATH, "rb"))
FEATURE_COLUMNS = pickle.load(open(FEATURE_PATH, "rb"))

# ================= GLOBAL =================
WORKERS_DF = pd.DataFrame()
JOBS_DF = pd.DataFrame()
WORKER_VEC = np.array([])
JOB_VEC = np.array([])

# ================= SAFE FLOAT =================
def safe_float(val, default=0.0):
    try:
        if val is None or np.isnan(val) or np.isinf(val):
            return default
        return float(val)
    except:
        return default

# ================= LOAD =================
def load_data():
    with engine.connect() as conn:
        workers = pd.read_sql("SELECT * FROM workers", conn)
        jobs = pd.read_sql('SELECT * FROM "Jobs"', conn)

    workers["id"] = workers["id"].astype(str)
    jobs["id"] = jobs["id"].astype(str)

    workers["rating"] = workers["rating"].fillna(0)
    jobs["budget"] = jobs["budget"].fillna(0)

    return workers, jobs

def convert_embeddings(df, col):
    vectors = []
    for v in df[col]:
        try:
            if isinstance(v, str):
                vectors.append(np.array(ast.literal_eval(v)))
            elif isinstance(v, list):
                vectors.append(np.array(v))
            else:
                vectors.append(np.zeros(384))
        except:
            vectors.append(np.zeros(384))
    return np.array(vectors)

def refresh_data():
    global WORKERS_DF, JOBS_DF, WORKER_VEC, JOB_VEC
    WORKERS_DF, JOBS_DF = load_data()
    WORKER_VEC = convert_embeddings(WORKERS_DF, "worker_embedding")
    JOB_VEC = convert_embeddings(JOBS_DF, "job_embedding")

refresh_data()

# ================= DISTANCE =================
def haversine(lat1, lon1, lat2, lon2):
    try:
        R = 6371
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
        return safe_float(R * 2 * np.arcsin(np.sqrt(a)), 999)
    except:
        return 999

# ================= MAIN =================
def recommend_workers_for_job(job_id, top_n=5):

    refresh_data()

    job_match = JOBS_DF[JOBS_DF["id"] == job_id]
    if job_match.empty:
        return []

    job_row = job_match.iloc[0]
    job_idx = JOBS_DF.index[JOBS_DF["id"] == job_id][0]

    job_vector = JOB_VEC[job_idx].reshape(1, -1)
    similarities = cosine_similarity(job_vector, WORKER_VEC)[0]

    recommendations = []

    for i, worker in WORKERS_DF.iterrows():

        similarity = safe_float(similarities[i])
        similarity = max(0, min(1, similarity))

        if similarity < SIMILARITY_THRESHOLD:
            continue

        dist = haversine(
            worker["location_lat"],
            worker["location_lng"],
            job_row["location_lat"],
            job_row["location_lng"]
        )

        if dist > MAX_DISTANCE_KM:
            continue

        exp = safe_float(worker.get("experience_years", 0))
        rating = safe_float(worker.get("rating", 0))
        budget = safe_float(job_row.get("budget", 0))
        status = job_row.get("status", "open")

        features = {
            "skill_similarity": similarity,
            "experience_bucket": 0 if exp <= 2 else (1 if exp <= 5 else 2),
            "avg_rating": rating,
            "distance_km": dist,
            "budget": budget,
        }

        for col in FEATURE_COLUMNS:
            if col.startswith("status_"):
                features[col] = 1 if col == f"status_{status}" else 0

        for col in FEATURE_COLUMNS:
            if col not in features:
                features[col] = 0

        X = pd.DataFrame([features])[FEATURE_COLUMNS]

        try:
            ml_score = safe_float(MODEL.predict(X)[0])
        except:
            ml_score = 0.0

        final_score = safe_float(
            0.6 * ml_score +
            0.2 * similarity +
            0.2 * (rating / 5)
        )

        recommendations.append({
            "worker_id": str(worker["id"]),
            "final_score": round(final_score, 3),
            "ml_score": round(ml_score, 3),
            "similarity": round(similarity, 3),
            "distance_km": round(dist, 2),
            "rating": round(rating, 2),
            "full_name": worker.get("full_name", "")
        })

    return sorted(recommendations, key=lambda x: x["final_score"], reverse=True)[:top_n]