import os
import ast
import pickle
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity

# --- CONFIG ---
SIMILARITY_THRESHOLD = 0.10
MAX_DISTANCE_KM = 100

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

# -------------------------------
# LOAD ML MODEL
# -------------------------------
MODEL = pickle.load(open("predictive_model.pkl", "rb"))
FEATURE_COLUMNS = pickle.load(open("feature_columns.pkl", "rb"))

# -------------------------------
# LOAD DATA
# -------------------------------
def load_data():
    with engine.connect() as conn:
        workers = pd.read_sql("SELECT * FROM workers", conn)
        jobs = pd.read_sql('SELECT * FROM "Jobs"', conn)

    workers["id"] = workers["id"].astype(str)
    jobs["id"] = jobs["id"].astype(str)

    workers["rating"] = workers["rating"].fillna(0)
    jobs["budget"] = jobs["budget"].fillna(0)

    return workers, jobs


def load_skills():
    with engine.connect() as conn:
        worker_skills = pd.read_sql(
            'SELECT worker_id, skill_id FROM "Worker_skills"', conn
        )
        job_skills = pd.read_sql(
            'SELECT job_id, skill_id FROM "job_required_skills"', conn
        )

    worker_skills["worker_id"] = worker_skills["worker_id"].astype(str)
    job_skills["job_id"] = job_skills["job_id"].astype(str)

    return worker_skills, job_skills


# -------------------------------
# EMBEDDINGS
# -------------------------------
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


# -------------------------------
# GLOBAL LOAD
# -------------------------------
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


# -------------------------------
# DISTANCE
# -------------------------------
def haversine(lat1, lon1, lat2, lon2):
    try:
        R = 6371
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        return R * c
    except:
        return 999


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def recommend_workers_for_job(job_id, top_n=5):

    refresh_data()

    job_match = JOBS_DF[JOBS_DF["id"] == job_id]
    if job_match.empty:
        return []

    job_row = job_match.iloc[0]
    job_idx = JOBS_DF.index[JOBS_DF["id"] == job_id][0]

    job_vector = JOB_VEC[job_idx].reshape(1, -1)
    similarities = cosine_similarity(job_vector, WORKER_VEC)[0]

    # -------------------------
    # SKILL MAPS
    # -------------------------
    job_skills = set(
        JOB_SKILLS_DF[JOB_SKILLS_DF["job_id"] == job_id]["skill_id"].astype(str)
    )

    worker_skill_map = (
        WORKER_SKILLS_DF.groupby("worker_id")["skill_id"]
        .apply(lambda x: set(x.astype(str)))
        .to_dict()
    )

    recommendations = []

    for i, worker in WORKERS_DF.iterrows():

        worker_id = str(worker["id"])
        worker_skills = worker_skill_map.get(worker_id, set())

        # -------------------------
        # 1. STRICT SKILL FILTER
        # -------------------------
        if len(worker_skills.intersection(job_skills)) == 0:
            continue

        # -------------------------
        # 2. EMBEDDING FILTER
        # -------------------------
        similarity = float(similarities[i])
        similarity = max(0, min(1, similarity))

        if similarity < SIMILARITY_THRESHOLD:
            continue

        # -------------------------
        # 3. DISTANCE FILTER
        # -------------------------
        dist = haversine(
            worker["location_lat"],
            worker["location_lng"],
            job_row["location_lat"],
            job_row["location_lng"]
        )

        if dist > MAX_DISTANCE_KM:
            continue

        # -------------------------
        # 4. SAFE VALUES
        # -------------------------
        exp = worker.get("experience_years", 0) or 0
        rating = worker.get("rating", 0) or 0
        budget = job_row.get("budget", 0) or 0
        status = job_row.get("status", "open")

        # -------------------------
        # 5. ML FEATURES
        # -------------------------
        features = {
            "skill_similarity": similarity,
            "experience_bucket": 0 if exp <= 2 else (1 if exp <= 5 else 2),
            "avg_rating": rating,
            "distance_km": dist,
            "budget": budget,
        }

        # status encoding
        for col in FEATURE_COLUMNS:
            if col.startswith("status_"):
                features[col] = 1 if col == f"status_{status}" else 0

        # fill missing
        for col in FEATURE_COLUMNS:
            if col not in features:
                features[col] = 0

        X = pd.DataFrame([features])[FEATURE_COLUMNS]

        # -------------------------
        # 6. ML PREDICTION
        # -------------------------
        final_score = MODEL.predict(X)[0]

        recommendations.append({
            "worker_id": worker_id,
            "ml_score": round(float(final_score), 3),
            "similarity": round(similarity, 3),
            "distance_km": round(float(dist), 2),
            "rating": float(rating)
        })

    # -------------------------
    # 7. FINAL SORT
    # -------------------------
    return sorted(
        recommendations,
        key=lambda x: x["ml_score"],
        reverse=True
    )[:top_n]


# -------------------------------
# TEST
# -------------------------------
if __name__ == "__main__":
    result = recommend_workers_for_job("PUT_JOB_ID_HERE")
    print(result)