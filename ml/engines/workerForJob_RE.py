import os
import ast
import pickle
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from ml.engines.model_validator import predict_score

# --- CONFIGURATION ---
SIMILARITY_THRESHOLD = 0.45
MAX_DISTANCE_KM = 20

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load KMeans once at startup
kmeans = pickle.load(open(os.path.join(MODEL_DIR, "kmeans_model.pkl"), "rb"))

def load_data():
    with engine.connect() as connection:
        # This 'with' block automatically handles connection closing/rollbacks
        workers = pd.read_sql("SELECT * FROM workers", connection)
        jobs = pd.read_sql('SELECT * FROM "Jobs"', connection)
    
    workers["id"] = workers["id"].astype(str)
    jobs["id"] = jobs["id"].astype(str)
    # Fill NaNs to prevent the JSON crash we saw earlier
    workers["rating"] = workers["rating"].fillna(0)
    jobs["budget"] = jobs["budget"].fillna(0)
    return workers, jobs

def load_skills():
    with engine.connect() as connection:
        worker_skills = pd.read_sql('SELECT * FROM "Worker_skills"', connection)
        job_skills = pd.read_sql('SELECT * FROM "Job_required_skill"', connection)
        
    worker_skills["worker_id"] = worker_skills["worker_id"].astype(str)
    job_skills["job_id"] = job_skills["job_id"].astype(str)
    return worker_skills, job_skills
def convert_embeddings(df, column):
    vectors = []
    for v in df[column]:
        if isinstance(v, str):
            vectors.append(np.array(ast.literal_eval(v)))
        elif isinstance(v, list):
            vectors.append(np.array(v))
        else:
            vectors.append(np.zeros(384))
    return np.array(vectors)

WORKERS_DF, JOBS_DF = load_data()
WORKER_SKILLS_DF, JOB_SKILLS_DF = load_skills()
WORKER_VEC = convert_embeddings(WORKERS_DF, "worker_embedding")
JOB_VEC = convert_embeddings(JOBS_DF, "job_embedding")

def refresh_data():
    global WORKERS_DF, JOBS_DF, WORKER_SKILLS_DF, JOB_SKILLS_DF, WORKER_VEC, JOB_VEC
    WORKERS_DF, JOBS_DF = load_data()
    WORKER_SKILLS_DF, JOB_SKILLS_DF = load_skills()
    WORKER_VEC = convert_embeddings(WORKERS_DF, "worker_embedding")
    JOB_VEC = convert_embeddings(JOBS_DF, "job_embedding")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def recommend_workers_for_job(job_id, top_n=5):
    refresh_data()
    global JOBS_DF, WORKERS_DF, WORKER_VEC, JOB_VEC

    job_match = JOBS_DF[JOBS_DF["id"] == job_id]
    if job_match.empty: return []

    job_row = job_match.iloc[0]
    job_idx = JOBS_DF.index[JOBS_DF["id"] == job_id][0]
    job_vector = JOB_VEC[job_idx].reshape(1, -1)

    similarities = cosine_similarity(job_vector, WORKER_VEC)[0]
    job_skills = set(JOB_SKILLS_DF[JOB_SKILLS_DF["job_id"] == job_id]["skill_id"])
    eligible_ids = set(WORKER_SKILLS_DF[WORKER_SKILLS_DF["skill_id"].isin(job_skills)]["worker_id"])

    candidates = []
    for i, worker in WORKERS_DF.iterrows():
        if worker["id"] not in eligible_ids: continue
        
        similarity = float(similarities[i])
        if similarity < SIMILARITY_THRESHOLD: continue

        dist = haversine(worker["location_lat"], worker["location_lng"], job_row["location_lat"], job_row["location_lng"])
        if dist > MAX_DISTANCE_KM: continue

        # Ensure numeric stability for JSON
        safe_similarity = round(similarity, 3) if not np.isnan(similarity) else 0.0
        safe_dist = round(float(dist), 3) if not np.isnan(dist) else 0.0

        candidates.append({
            "worker_id": str(worker["id"]),
            "score": safe_similarity,
            "distance_km": safe_dist,
            "rating": float(worker["rating"]),
            "similarity": safe_similarity
        })

    return sorted(candidates, key=lambda x: x["score"], reverse=True)[:top_n]