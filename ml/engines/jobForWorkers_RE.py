import os
import ast
import pickle
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity

# --- CONFIGURATION ---
SIMILARITY_THRESHOLD = 0.30  # Keep this at 0.45 for quality!
MAX_DISTANCE_KM = 100

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def load_data():
    workers = pd.read_sql("SELECT * FROM workers", engine)
    jobs = pd.read_sql('SELECT * FROM "Jobs"', engine)
    workers["id"] = workers["id"].astype(str)
    jobs["id"] = jobs["id"].astype(str)
    return workers, jobs

def load_skills():
    worker_skills = pd.read_sql('SELECT * FROM "Worker_skills"', engine)
    job_skills = pd.read_sql('SELECT * FROM "Job_required_skill"', engine)
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

# Global variables for memory
WORKERS_DF, JOBS_DF = load_data()
WORKER_SKILLS_DF, JOB_SKILLS_DF = load_skills()
WORKER_VEC = convert_embeddings(WORKERS_DF, "worker_embedding")
JOB_VEC = convert_embeddings(JOBS_DF, "job_embedding")

def refresh_data():
    """Fetches the latest data from Supabase into memory."""
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
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def recommend_jobs_for_worker(worker_id, top_n=5):
    global WORKERS_DF, JOBS_DF, WORKER_VEC, JOB_VEC

    # 1. Refresh if worker is new (Cold Start Fix)
    if worker_id not in WORKERS_DF["id"].values:
        refresh_data()

    worker_match = WORKERS_DF[WORKERS_DF["id"] == worker_id]
    if worker_match.empty:
        return []

    worker_row = worker_match.iloc[0]
    worker_idx = WORKERS_DF.index[WORKERS_DF["id"] == worker_id][0]
    worker_vector = WORKER_VEC[worker_idx].reshape(1, -1)

    # Calculate AI similarities
    similarities = cosine_similarity(worker_vector, JOB_VEC)[0]
    worker_skills = set(WORKER_SKILLS_DF[WORKER_SKILLS_DF["worker_id"] == worker_id]["skill_id"])

    recommendations = []

    for i, job in JOBS_DF.iterrows():
        # Skill Filter
        job_skills = set(JOB_SKILLS_DF[JOB_SKILLS_DF["job_id"] == job["id"]]["skill_id"])
        if not (worker_skills & job_skills):
            continue

        # AI Similarity Filter
        similarity = similarities[i]
        if similarity < SIMILARITY_THRESHOLD:
            continue

        # Distance Filter
        distance = haversine(worker_row["location_lat"], worker_row["location_lng"], 
                             job["location_lat"], job["location_lng"])
        if distance > MAX_DISTANCE_KM:
            continue

        recommendations.append({
            "job_id": job["id"],
            "title": job["title"],
            "score": round(float(similarity), 3),
            "distance_km": round(float(distance), 3),
            "budget": job["budget"]
        })

    return sorted(recommendations, key=lambda x: x["score"], reverse=True)[:top_n]