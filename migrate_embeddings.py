from dotenv import load_dotenv
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
import os

# -----------------------------
# Setup
# -----------------------------
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

# -----------------------------
# FILE PATHS
# -----------------------------
WORKERS_CSV = "data/raw/workers_df.csv"
WORKER_VECTORS = "ml/vectors/worker_vectors.npy"

JOBS_CSV = "data/raw/jobs_df.csv"
JOB_VECTORS = "ml/vectors/job_vectors.npy"


# -----------------------------
# LOAD WORKERS
# -----------------------------
print("Loading workers...")
workers_df = pd.read_csv(WORKERS_CSV)
worker_vectors = np.load(WORKER_VECTORS)

print("Worker shape:", worker_vectors.shape)

assert len(workers_df) == len(worker_vectors), \
    "Workers CSV and vector count mismatch!"

# -----------------------------
# LOAD JOBS
# -----------------------------
print("Loading jobs...")
jobs_df = pd.read_csv(JOBS_CSV)
job_vectors = np.load(JOB_VECTORS)

print("Job shape:", job_vectors.shape)

assert len(jobs_df) == len(job_vectors), \
    "Jobs CSV and vector count mismatch!"

# -----------------------------
# MIGRATE WORKERS
# -----------------------------
print("Migrating worker embeddings...")

with engine.begin() as conn:
    for i in range(len(workers_df)):
        worker_id = workers_df.iloc[i]["id"]
        embedding_str = str(worker_vectors[i].tolist())

        conn.execute(
            text("""
                UPDATE workers
                SET worker_embedding = :embedding
                WHERE id = :id
            """),
            {"embedding": embedding_str, "id": worker_id}
        )

print("Worker migration complete.")


# -----------------------------
# MIGRATE JOBS
# -----------------------------
print("Migrating job embeddings...")

with engine.begin() as conn:
    for i in range(len(jobs_df)):
        job_id = jobs_df.iloc[i]["id"]
        embedding_str = str(job_vectors[i].tolist())

        conn.execute(
            text("""
                UPDATE "Jobs"
                SET job_embedding = :embedding
                WHERE id = :id
            """),
            {"embedding": embedding_str, "id": job_id}
        )

print("Job migration complete.")

print("🎉 ALL MIGRATIONS COMPLETED SUCCESSFULLY.")