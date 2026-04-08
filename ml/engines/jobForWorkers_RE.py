import os
import ast
import numpy as np
import pandas as pd
import pickle
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity

# --- CONFIGURATION ---
SIMILARITY_THRESHOLD = 0.1
MAX_DISTANCE_KM = 100

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

# --- GLOBAL DATA ---
WORKERS_DF = pd.DataFrame()
JOBS_DF = pd.DataFrame()
WORKER_VEC = np.array([])
JOB_VEC = np.array([])

# --- LOAD ML MODEL ---
MODEL = pickle.load(open("predictive_model.pkl", "rb"))
FEATURE_COLUMNS = pickle.load(open("feature_columns.pkl", "rb"))

# -------------------------------------------------
# LOAD SKILLS (OPTIMIZED)
# -------------------------------------------------

def load_job_skills():
    query = 'SELECT job_id, skill_id FROM "Job_required_skills"'
    df = pd.read_sql(query, engine)

    job_skill_map = {}
    for _, row in df.iterrows():
        job_id = str(row["job_id"])
        skill_id = str(row["skill_id"])
        job_skill_map.setdefault(job_id, set()).add(skill_id)

    return job_skill_map


JOB_SKILL_MAP = load_job_skills()

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def get_worker_skills(worker_id):
    query = 'SELECT skill_id FROM "Worker_skills" WHERE worker_id = %s'
    df = pd.read_sql(query, engine, params=(worker_id,))
    return set(df["skill_id"].astype(str).tolist())


def load_data():
    with engine.connect() as connection:
        workers = pd.read_sql("SELECT * FROM workers", connection)
        jobs = pd.read_sql('SELECT * FROM "Jobs"', connection)

    workers["id"] = workers["id"].astype(str)
    jobs["id"] = jobs["id"].astype(str)

    workers["rating"] = workers["rating"].fillna(0)
    jobs["budget"] = jobs["budget"].fillna(0)

    return workers, jobs


def convert_embeddings(df, column):
    vectors = []

    if df.empty:
        return np.array([])

    for v in df[column]:
        if isinstance(v, str):
            vectors.append(np.array(ast.literal_eval(v)))
        elif isinstance(v, list):
            vectors.append(np.array(v))
        else:
            vectors.append(np.zeros(384))

    return np.array(vectors)


def refresh_data():
    global WORKERS_DF, JOBS_DF, WORKER_VEC, JOB_VEC
    WORKERS_DF, JOBS_DF = load_data()
    WORKER_VEC = convert_embeddings(WORKERS_DF, "worker_embedding")
    JOB_VEC = convert_embeddings(JOBS_DF, "job_embedding")


# Initial load
refresh_data()


def haversine(lat1, lon1, lat2, lon2):
    R = 6371

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


# =================================================
# 🎯 MAIN RECOMMENDATION FUNCTION
# =================================================

def recommend_jobs_for_worker(worker_id, top_n=5):

    refresh_data()

    worker_match = WORKERS_DF[WORKERS_DF["id"] == worker_id]
    if worker_match.empty:
        return []

    worker_row = worker_match.iloc[0]
    worker_idx = WORKERS_DF.index[WORKERS_DF["id"] == worker_id][0]

    worker_vector = WORKER_VEC[worker_idx].reshape(1, -1)
    similarities = cosine_similarity(worker_vector, JOB_VEC)[0]

    worker_skills = get_worker_skills(worker_id)

    recommendations = []

    for i, job in JOBS_DF.iterrows():

        job_id = str(job["id"])
        job_skills = JOB_SKILL_MAP.get(job_id, set())

        # -------------------------
        # 1. STRICT SKILL FILTER
        # -------------------------
        common_skills = worker_skills.intersection(job_skills)

        if len(common_skills) == 0:
            continue

        # -------------------------
        # 2. SKILL SIMILARITY (FIXED)
        # -------------------------
        skill_similarity_score = len(common_skills) / max(len(job_skills), 1)

        # -------------------------
        # 3. EMBEDDING SIMILARITY
        # -------------------------
        similarity = float(similarities[i])
        similarity = max(0, min(1, similarity))

        if similarity < SIMILARITY_THRESHOLD:
            continue

        # -------------------------
        # 4. DISTANCE FILTER
        # -------------------------
        try:
            dist = haversine(
                worker_row["location_lat"],
                worker_row["location_lng"],
                job["location_lat"],
                job["location_lng"]
            )
        except:
            dist = 999

        if dist > MAX_DISTANCE_KM:
            continue

        # -------------------------
        # 5. SAFE VALUES
        # -------------------------
        exp = worker_row.get("experience_years", 0) or 0
        rating = worker_row.get("rating", 0) or 0
        budget = job.get("budget", 0) or 0
        status = job.get("status", "unknown")

        # -------------------------
        # 6. ML FEATURES
        # -------------------------
        features = {
            "skill_similarity": skill_similarity_score,  # ✅ FIXED
            "experience_bucket": 0 if exp <= 2 else (1 if exp <= 5 else 2),
            "avg_rating": rating,
            "distance_km": dist,
            "budget": budget,
        }

        # status encoding
        for col in FEATURE_COLUMNS:
            if col.startswith("status_"):
                features[col] = 1 if col == f"status_{status}" else 0

        # fill missing columns
        for col in FEATURE_COLUMNS:
            if col not in features:
                features[col] = 0

        X = pd.DataFrame([features])[FEATURE_COLUMNS]

        # -------------------------
        # 7. ML PREDICTION
        # -------------------------
        final_score = MODEL.predict(X)[0]

        recommendations.append({
            "job_id": job_id,
            "title": job["title"],
            "ml_score": round(float(final_score), 3),
            "skill_match": round(skill_similarity_score, 2),
            "similarity": round(similarity, 3),
            "distance_km": round(float(dist), 2),
            "budget": float(budget)
        })

    # -------------------------
    # 8. FINAL SORT
    # -------------------------
    return sorted(
        recommendations,
        key=lambda x: x["ml_score"],
        reverse=True
    )[:top_n]


# =================================================
# 🧪 TEST
# =================================================

if __name__ == "__main__":
    result = recommend_jobs_for_worker("2d38f749-8d4a-4867-8df0-88b211c89df8")
    print(result)