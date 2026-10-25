import os
import numpy as np
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Configure it in your environment."
    )

print("Loading embeddings...")

# Load embeddings
worker_vectors = np.load("worker_vectors.npy")
job_vectors = np.load("job_vectors.npy")

# Load sentence mapping files
worker_sent_df = pd.read_csv(
    "worker_skill_sentences.csv",
    dtype={"worker_id": str}
)
job_sent_df = pd.read_csv(
    "job_skill_sentences.csv",
    dtype={"job_id": str}
)

print("Worker vectors shape:", worker_vectors.shape)
print("Job vectors shape:", job_vectors.shape)

# Validate row alignment before making database changes
if len(worker_sent_df) != len(worker_vectors):
    raise ValueError(
        "Worker sentence rows do not match worker embedding count."
    )

if len(job_sent_df) != len(job_vectors):
    raise ValueError(
        "Job sentence rows do not match job embedding count."
    )

conn = None
cursor = None

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    print("Updating worker embeddings...")

    for i, row in worker_sent_df.iterrows():
        worker_id = row["worker_id"]

        if pd.isna(worker_id) or not str(worker_id).strip():
            continue

        vector = [float(value) for value in worker_vectors[i]]

        cursor.execute(
            """
            UPDATE workers
            SET worker_embedding = %s
            WHERE id = %s
            """,
            (vector, str(worker_id))
        )

    print("Worker embeddings updated.")

    print("Updating job embeddings...")

    for i, row in job_sent_df.iterrows():
        job_id = row["job_id"]

        if pd.isna(job_id) or not str(job_id).strip():
            continue

        vector = [float(value) for value in job_vectors[i]]

        cursor.execute(
            """
            UPDATE "Jobs"
            SET job_embedding = %s
            WHERE id = %s
            """,
            (vector, str(job_id))
        )

    conn.commit()
    print("Embeddings uploaded successfully.")

except Exception:
    if conn is not None:
        conn.rollback()

    # Avoid printing database URLs or credentials.
    print("Embedding upload failed. Transaction rolled back.")
    raise

finally:
    if cursor is not None:
        cursor.close()

    if conn is not None:
        conn.close()