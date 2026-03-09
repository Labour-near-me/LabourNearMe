import os
import ast
import pickle
import numpy as np
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity

from ml.engines.model_validator import predict_score


SIMILARITY_THRESHOLD = 0.45
MAX_DISTANCE_KM = 20


load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

kmeans = pickle.load(open(os.path.join(MODEL_DIR, "kmeans_model.pkl"), "rb"))


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


def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def recommend_workers_for_job(job_id, top_n=5):

    job_row = JOBS_DF[JOBS_DF["id"] == job_id].iloc[0]

    job_vector = JOB_VEC[JOBS_DF.index[JOBS_DF["id"] == job_id][0]].reshape(1, -1)

    similarities = cosine_similarity(job_vector, WORKER_VEC)[0]

    job_skills = set(
        JOB_SKILLS_DF[JOB_SKILLS_DF["job_id"] == job_id]["skill_id"]
    )

    eligible_workers = set(
        WORKER_SKILLS_DF[
            WORKER_SKILLS_DF["skill_id"].isin(job_skills)
        ]["worker_id"]
    )

    candidates = []

    for i, worker in WORKERS_DF.iterrows():

        if worker["id"] not in eligible_workers:
            continue

        similarity = similarities[i]

        if similarity < SIMILARITY_THRESHOLD:
            continue

        distance = haversine(
            worker["location_lat"],
            worker["location_lng"],
            job_row["location_lat"],
            job_row["location_lng"]
        )

        if distance > MAX_DISTANCE_KM:
            continue

        experience_bucket = 0
        if worker["experience_years"] > 5:
            experience_bucket = 2
        elif worker["experience_years"] > 2:
            experience_bucket = 1

        vector = np.array(WORKER_VEC[i], dtype=np.float64).reshape(1, -1)
        worker_cluster = int(kmeans.predict(vector)[0])

        features = pd.DataFrame([{
            "skill_similarity": similarity,
            "experience_bucket": experience_bucket,
            "avg_rating": worker["rating"],
            "distance_km": distance,
            "budget": job_row["budget"],
            "status": job_row["status"],
            "worker_cluster": worker_cluster
        }])

        predictive_score = float(predict_score(features)) / 5
        print("Prediction:", predictive_score)

        rating_score = worker["rating"] / 5
        proximity_score = 1 / (1 + distance)

        matched_skills = len(
            WORKER_SKILLS_DF[
                (WORKER_SKILLS_DF["worker_id"] == worker["id"]) &
                (WORKER_SKILLS_DF["skill_id"].isin(job_skills))
            ]
        )

        skill_boost = matched_skills / max(len(job_skills), 1)

        final_score = (
            0.35 * similarity +
            0.20 * rating_score +
            0.20 * proximity_score +
            0.15 * predictive_score +
            0.10 * skill_boost
        )

        candidates.append({
            "worker_id": worker["id"],
            "score": round(float(final_score), 3),
            "distance_km": round(float(distance), 3),
            "rating": round(float(worker["rating"]), 2),
            "similarity": round(float(similarity), 3),
            "predictive_score": round(float(predictive_score), 3),
            "matched_skills": matched_skills
        })

    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)

    return candidates[:top_n]


WORKERS_DF, JOBS_DF = load_data()
WORKER_SKILLS_DF, JOB_SKILLS_DF = load_skills()

WORKER_VEC = convert_embeddings(WORKERS_DF, "worker_embedding")
JOB_VEC = convert_embeddings(JOBS_DF, "job_embedding")


if __name__ == "__main__":
    print("\n✅ Predictive model loaded")
    print("Testing worker recommendation engine with random samples...\n")

    # Pick 3 random jobs from the database to see variety
    test_jobs = JOBS_DF.sample(3)

    for _, job in test_jobs.iterrows():
        print(f"\n--- Recommended workers for: {job['title']} ({job['id']}) ---")
        
        results = recommend_workers_for_job(job['id'], top_n=5)

        if not results:
            print("No suitable workers found for this job category.")
        for r in results:
            print(r)