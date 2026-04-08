import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os
import ast

# -------------------------------
# CONFIG
# -------------------------------
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

SIMILARITY_THRESHOLD = 0.1
MAX_DISTANCE_KM = 100
TOP_N = 5

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
            'SELECT job_id, skill_id FROM "Job_required_skill"', conn
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
# WORKER → JOB (TOP 5)
# -------------------------------
def validate_worker(worker_id, workers, jobs, worker_vec, job_vec, worker_skills_df, job_skills_df):

    print("\n==============================")
    print("🔍 WORKER → JOB (TOP 5)")
    print("==============================")

    worker_row = workers[workers["id"] == worker_id]
    if worker_row.empty:
        print("❌ Worker not found")
        return

    worker_row = worker_row.iloc[0]
    worker_idx = workers.index[workers["id"] == worker_id][0]

    similarities = cosine_similarity(
        worker_vec[worker_idx].reshape(1, -1),
        job_vec
    )[0]

    worker_skills = set(
        worker_skills_df[worker_skills_df["worker_id"] == worker_id]["skill_id"].astype(str)
    )

    job_skill_map = (
        job_skills_df.groupby("job_id")["skill_id"]
        .apply(lambda x: set(x.astype(str)))
        .to_dict()
    )

    results = []

    for i, job in jobs.iterrows():
        job_id = str(job["id"])
        job_skills = job_skill_map.get(job_id, set())

        if not worker_skills.intersection(job_skills):
            continue

        similarity = float(similarities[i])
        dist = haversine(
            worker_row["location_lat"],
            worker_row["location_lng"],
            job["location_lat"],
            job["location_lng"]
        )

        if similarity < SIMILARITY_THRESHOLD or dist > MAX_DISTANCE_KM:
            continue

        results.append({
            "job": job["title"],
            "similarity": similarity,
            "distance": dist
        })

    # 🔥 TOP 5
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:TOP_N]

    for r in results:
        print("\nJob:", r["job"])
        print("Similarity:", round(r["similarity"], 3))
        print("Distance:", round(r["distance"], 2))

    print("\n✅ Total shown:", len(results))


# -------------------------------
# JOB → WORKER (TOP 5)
# -------------------------------
def validate_job(job_id, workers, jobs, worker_vec, job_vec, worker_skills_df, job_skills_df):

    print("\n==============================")
    print("🔍 JOB → WORKER (TOP 5)")
    print("==============================")

    job_row = jobs[jobs["id"] == job_id]
    if job_row.empty:
        print("❌ Job not found")
        return

    job_row = job_row.iloc[0]
    job_idx = jobs.index[jobs["id"] == job_id][0]

    similarities = cosine_similarity(
        job_vec[job_idx].reshape(1, -1),
        worker_vec
    )[0]

    job_skills = set(
        job_skills_df[job_skills_df["job_id"] == job_id]["skill_id"].astype(str)
    )

    worker_skill_map = (
        worker_skills_df.groupby("worker_id")["skill_id"]
        .apply(lambda x: set(x.astype(str)))
        .to_dict()
    )

    results = []

    for i, worker in workers.iterrows():
        worker_id = str(worker["id"])
        worker_skills = worker_skill_map.get(worker_id, set())

        if not worker_skills.intersection(job_skills):
            continue

        similarity = float(similarities[i])
        dist = haversine(
            worker["location_lat"],
            worker["location_lng"],
            job_row["location_lat"],
            job_row["location_lng"]
        )

        if similarity < SIMILARITY_THRESHOLD or dist > MAX_DISTANCE_KM:
            continue

        results.append({
            "worker_id": worker_id,
            "similarity": similarity,
            "distance": dist,
            "rating": worker["rating"]
        })

    # 🔥 TOP 5
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:TOP_N]

    for r in results:
        print("\nWorker:", r["worker_id"])
        print("Similarity:", round(r["similarity"], 3))
        print("Distance:", round(r["distance"], 2))
        print("Rating:", r["rating"])

    print("\n✅ Total shown:", len(results))


# -------------------------------
# MASTER VALIDATOR
# -------------------------------
def validate_system(worker_id, job_id):

    workers, jobs = load_data()
    worker_skills_df, job_skills_df = load_skills()

    worker_vec = convert_embeddings(workers, "worker_embedding")
    job_vec = convert_embeddings(jobs, "job_embedding")

    validate_worker(worker_id, workers, jobs, worker_vec, job_vec, worker_skills_df, job_skills_df)
    validate_job(job_id, workers, jobs, worker_vec, job_vec, worker_skills_df, job_skills_df)

    print("\n==============================")
    print("✅ TOP-5 VALIDATION COMPLETE")
    print("==============================")


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    validate_system(
        worker_id="46c65985-3d7c-4fae-9276-7fac75fc9ff4",
        job_id="a82e72b8-f752-41cf-b7d7-60df77bfd9d4"
    )