import numpy as np
import pandas as pd
import psycopg2

print("Loading embeddings...")

worker_vectors = np.load("worker_vectors.npy")
job_vectors = np.load("job_vectors.npy")

workers_df = pd.read_csv("workers_df.csv", dtype={"id": str})
jobs_df = pd.read_csv("jobs_df.csv", dtype={"id": str})

print(worker_vectors.shape, job_vectors.shape)

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

for i, row in workers_df.iterrows():

    worker_id = str(row["id"])

    if worker_id == "nan":
        continue

    vector = worker_vectors[i].tolist()

    cursor.execute(
        """
        UPDATE workers
        SET worker_embedding = %s
        WHERE id = %s
        """,
        (vector, worker_id)
    )


# -------------------------
# Upload job embeddings
# -------------------------

print("Updating job embeddings...")

for i, row in jobs_df.iterrows():

    job_id = str(row["id"])

    if job_id == "nan":
        continue

    vector = job_vectors[i].tolist()

    cursor.execute(
        """
        UPDATE "Jobs"
        SET job_embedding = %s
        WHERE id = %s
        """,
        (vector, job_id)
    )


conn.commit()

cursor.close()
conn.close()

print("Embeddings uploaded successfully.")