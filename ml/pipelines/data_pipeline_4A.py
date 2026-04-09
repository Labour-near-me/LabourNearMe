import numpy as np
import pandas as pd
import psycopg2

print("Loading embeddings...")

# Load embeddings
worker_vectors = np.load("worker_vectors.npy")
job_vectors = np.load("job_vectors.npy")

# Load sentence mapping files (IMPORTANT FIX)
worker_sent_df = pd.read_csv("worker_skill_sentences.csv", dtype={"worker_id": str})
job_sent_df = pd.read_csv("job_skill_sentences.csv", dtype={"job_id": str})

print("Worker vectors shape:", worker_vectors.shape)
print("Job vectors shape:", job_vectors.shape)

# DB Connection
conn = psycopg2.connect(
    host="aws-1-ap-south-1.pooler.supabase.com",
    database="postgres",
    user="postgres.ihnlpiujpjslpgesqimj",
    password="subArAshii325",
    port="6543"
)

cursor = conn.cursor()

# -------------------------
# Upload worker embeddings
# -------------------------

print("Updating worker embeddings...")

for i, row in worker_sent_df.iterrows():

    worker_id = str(row["worker_id"])

    if worker_id == "nan":
        continue

    vector = list(map(float, worker_vectors[i]))

    cursor.execute(
        """
        UPDATE workers
        SET worker_embedding = %s
        WHERE id = %s
        """,
        (vector, worker_id)
    )

print("Worker embeddings updated.")

# -------------------------
# Upload job embeddings
# -------------------------

print("Updating job embeddings...")

for i, row in job_sent_df.iterrows():

    job_id = str(row["job_id"])

    if job_id == "nan":
        continue

    vector = list(map(float, job_vectors[i]))

    cursor.execute(
        """
        UPDATE "Jobs"
        SET job_embedding = %s
        WHERE id = %s
        """,
        (vector, job_id)
    )

print("Job embeddings updated.")

# Commit changes
conn.commit()

# Close connection
cursor.close()
conn.close()

print("Embeddings uploaded successfully.")