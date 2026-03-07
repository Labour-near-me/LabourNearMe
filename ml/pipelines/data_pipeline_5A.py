import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

print("Loading embeddings...")

# Load embedding vectors
worker_vectors = np.load("worker_vectors.npy")
job_vectors = np.load("job_vectors.npy")

print("Worker vectors:", worker_vectors.shape)
print("Job vectors:", job_vectors.shape)

# Load CSV datasets
workers_df = pd.read_csv("workers_df.csv")
jobs_df = pd.read_csv("jobs_df.csv")

# Extract IDs safely (first column always contains IDs)
worker_ids = workers_df.iloc[:, 0].astype(str).tolist()
job_ids = jobs_df.iloc[:, 0].astype(str).tolist()

print("Workers loaded:", len(worker_ids))
print("Jobs loaded:", len(job_ids))

# Safety check
if len(worker_ids) != worker_vectors.shape[0]:
    raise ValueError("Worker count mismatch between CSV and embeddings")

if len(job_ids) != job_vectors.shape[0]:
    raise ValueError("Job count mismatch between CSV and embeddings")

print("Computing cosine similarity matrix...")

similarity_matrix = cosine_similarity(worker_vectors, job_vectors)

print("Similarity matrix shape:", similarity_matrix.shape)

records = []

# Better threshold to reduce dataset size
SIMILARITY_THRESHOLD = 0.15

print("Filtering similarity pairs...")

for i, worker_id in enumerate(worker_ids):

    for j, job_id in enumerate(job_ids):

        similarity_score = similarity_matrix[i][j]

        if similarity_score >= SIMILARITY_THRESHOLD:

            records.append({
                "worker_id": worker_id,
                "job_id": job_id,
                "skill_similarity": float(similarity_score)
            })

print("Creating dataframe...")

similarity_df = pd.DataFrame(records)

print("Saving similarity dataset...")

similarity_df.to_csv("worker_job_similarity.csv", index=False)

print("Similarity dataset created successfully.")
print("Total matches:", len(similarity_df))

print("\nSample rows:")
print(similarity_df.head())