import os
import ast
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity

# --- CONFIGURATION ---
SIMILARITY_THRESHOLD = 0.20  
MAX_DISTANCE_KM = 100

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

# Global variables initialized as empty
WORKERS_DF = pd.DataFrame()
JOBS_DF = pd.DataFrame()
WORKER_VEC = np.array([])
JOB_VEC = np.array([])

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
    
def convert_embeddings(df, column):
    vectors = []
    if df.empty: return np.array([])
    for v in df[column]:
        if isinstance(v, str): vectors.append(np.array(ast.literal_eval(v)))
        elif isinstance(v, list): vectors.append(np.array(v))
        else: vectors.append(np.zeros(384))
    return np.array(vectors)

def refresh_data():
    """This is the function your backend was missing!"""
    global WORKERS_DF, JOBS_DF, WORKER_VEC, JOB_VEC
    WORKERS_DF, JOBS_DF = load_data()
    WORKER_VEC = convert_embeddings(WORKERS_DF, "worker_embedding")
    JOB_VEC = convert_embeddings(JOBS_DF, "job_embedding")

# Initial Load
refresh_data()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def recommend_jobs_for_worker(worker_id, top_n=5):
    refresh_data() # Ensure fresh data for every request
    global WORKERS_DF, JOBS_DF, WORKER_VEC, JOB_VEC

    worker_match = WORKERS_DF[WORKERS_DF["id"] == worker_id]
    if worker_match.empty: return []

    worker_row = worker_match.iloc[0]
    worker_idx = WORKERS_DF.index[WORKERS_DF["id"] == worker_id][0]
    worker_vector = WORKER_VEC[worker_idx].reshape(1, -1)

    similarities = cosine_similarity(worker_vector, JOB_VEC)[0]
    
    recommendations = []
    for i, job in JOBS_DF.iterrows():
        similarity = float(similarities[i])
        if similarity < SIMILARITY_THRESHOLD: continue

        dist = haversine(worker_row["location_lat"], worker_row["location_lng"], 
                         job["location_lat"], job["location_lng"])
        
        if dist > MAX_DISTANCE_KM: continue

        recommendations.append({
            "job_id": str(job["id"]),
            "title": job["title"],
            "score": round(similarity, 3),
            "distance_km": round(float(dist), 3),
            "budget": float(job["budget"])
        })

    return sorted(recommendations, key=lambda x: x["score"], reverse=True)[:top_n]