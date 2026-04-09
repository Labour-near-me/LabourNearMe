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

SIMILARITY_THRESHOLD = 0.05
MAX_DISTANCE_KM = 300
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


# -------------------------------
# DISTANCE FUNCTION
# -------------------------------
def haversine(lat1, lon1, lat2, lon2):
    try:
        R = 6371
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        return R * 2 * np.arcsin(np.sqrt(
            np.sin((lat2 - lat1)/2)**2 +
            np.cos(lat1)*np.cos(lat2)*np.sin((lon2 - lon1)/2)**2
        ))
    except:
        return 999


# -------------------------------
# MAIN VALIDATOR
# -------------------------------
def validate_system(worker_id, job_id):

    workers, jobs = load_data()
    worker_skills_df, job_skills_df = load_skills()

    worker_vec = convert_embeddings(workers, "worker_embedding")
    job_vec = convert_embeddings(jobs, "job_embedding")

    print("\n🔥 DEBUG INFO")
    print("Workers:", len(workers))
    print("Jobs:", len(jobs))
    print("Worker vec shape:", worker_vec.shape)
    print("Job vec shape:", job_vec.shape)

    # -------------------------
    # WORKER → JOB
    # -------------------------
    print("\n========== WORKER → JOB ==========")

    worker_idx = workers.index[workers["id"] == worker_id][0]

    similarities = cosine_similarity(
        worker_vec[worker_idx].reshape(1, -1),
        job_vec
    )[0]

    results = []
    seen_jobs = set()

    for i, job in jobs.iterrows():

        similarity = float(similarities[i])
        job_title = job["title"]

        # ❌ skip duplicate job titles
        if job_title in seen_jobs:
            continue

        dist = haversine(
            workers.iloc[worker_idx]["location_lat"],
            workers.iloc[worker_idx]["location_lng"],
            job["location_lat"],
            job["location_lng"]
        )

        if similarity > 0:
            results.append({
                "job": job_title,
                "similarity": similarity,
                "distance": dist
            })
            seen_jobs.add(job_title)

    results = sorted(
                results,
                key=lambda x: (x["similarity"] * 0.7) - (x["distance"] * 0.01),
                reverse=True
            )[:TOP_N]

    for r in results:
        print(f"{r['job']} | sim={round(r['similarity'],3)} | dist={round(r['distance'],2)} km")

    print("\n✅ Total jobs shown:", len(results))

    # -------------------------
    # JOB → WORKER
    # -------------------------
    print("\n========== JOB → WORKER ==========")

    job_idx = jobs.index[jobs["id"] == job_id][0]

    similarities = cosine_similarity(
        job_vec[job_idx].reshape(1, -1),
        worker_vec
    )[0]

    results = []

    for i, worker in workers.iterrows():

        similarity = float(similarities[i])

        dist = haversine(
            worker["location_lat"],
            worker["location_lng"],
            jobs.iloc[job_idx]["location_lat"],
            jobs.iloc[job_idx]["location_lng"]
        )

        if similarity > 0:
            results.append({
                "worker_id": worker["id"],
                "similarity": similarity,
                "distance": dist,
                "rating": worker.get("rating", 0)
            })

    results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:TOP_N]

    for r in results:
        print(
            f"{r['worker_id']} | sim={round(r['similarity'],3)} | "
            f"dist={round(r['distance'],2)} km | rating={r['rating']}"
        )

    print("\n✅ Total workers shown:", len(results))

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