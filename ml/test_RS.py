import random
import pandas as pd

from ml.engines.workerForJob_RE import (
    recommend_workers_for_job,
    WORKERS_DF,
    JOBS_DF
)

from ml.engines.jobForWorkers_RE import (
    recommend_jobs_for_worker
)

# -----------------------------
# Load skill mappings
# -----------------------------
worker_skills = pd.read_csv("data/raw/worker_skills_df.csv", dtype=str)
job_skills = pd.read_csv("data/raw/job_skills_df.csv", dtype=str)
skill_master = pd.read_csv("data/raw/skill_master_df.csv", dtype=str)

# Normalize ID types
worker_skills["worker_id"] = worker_skills["worker_id"].astype(str)
worker_skills["skill_id"] = worker_skills["skill_id"].astype(str)

job_skills["job_id"] = job_skills["job_id"].astype(str)
job_skills["skill_id"] = job_skills["skill_id"].astype(str)

skill_master["id"] = skill_master["id"].astype(str)

# Convert skill_id → skill_name
skill_map = dict(zip(skill_master["id"], skill_master["skill_name"]))


# -----------------------------
# Helper Functions
# -----------------------------
def get_worker_skills(worker_id):
    worker_id = str(worker_id)
    skills = worker_skills.loc[
        worker_skills["worker_id"] == worker_id, "skill_id"
    ].tolist()

    return [skill_map.get(s, "unknown") for s in skills]


def get_job_skills(job_id):
    job_id = str(job_id)
    skills = job_skills.loc[
        job_skills["job_id"] == job_id, "skill_id"
    ].tolist()

    return [skill_map.get(s, "unknown") for s in skills]


# ==============================
# TEST 1
# JOB → WORKERS
# ==============================

print("\n==============================")
print("TEST 1: WORKERS FOR A JOB")
print("==============================")

random_job = JOBS_DF.sample(1).iloc[0]

job_id = str(random_job["id"])
job_title = random_job["title"]

print(f"\nJob Selected: {job_title}")

job_skill_list = get_job_skills(job_id)

print("\nRequired Skills:")
print(", ".join(job_skill_list) if job_skill_list else "No skills found")

workers = recommend_workers_for_job(job_id, top_n=5)

print("\nRecommended Workers:\n")

for i, w in enumerate(workers, 1):

    worker_id = str(w["worker_id"])
    worker_skill_list = get_worker_skills(worker_id)

    print(f"{i}. Worker ID: {worker_id}")
    print("   Skills:", ", ".join(worker_skill_list) if worker_skill_list else "No skills found")
    print(f"   Distance: {float(w['distance_km']):.2f} km")
    print(f"   Similarity: {float(w['similarity']):.2f}")
    print()


# ==============================
# TEST 2
# WORKER → JOBS
# ==============================

print("\n==============================")
print("TEST 2: JOBS FOR A WORKER")
print("==============================")

random_worker = WORKERS_DF.sample(1).iloc[0]

worker_id = str(random_worker["id"])

print(f"\nWorker Selected: {worker_id}")

worker_skill_list = get_worker_skills(worker_id)

print("\nWorker Skills:")
print(", ".join(worker_skill_list) if worker_skill_list else "No skills found")

jobs = recommend_jobs_for_worker(worker_id, top_n=5)

print("\nRecommended Jobs:\n")

for i, j in enumerate(jobs, 1):

    job_id = str(j["job_id"])
    job_skill_list = get_job_skills(job_id)

    print(f"{i}. {j['title']}")
    print("   Required Skills:", ", ".join(job_skill_list) if job_skill_list else "No skills found")
    print(f"   Distance: {float(j['distance_km']):.2f} km")
    print(f"   Similarity: {float(j['similarity']):.2f}")
    print()