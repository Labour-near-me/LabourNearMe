# =============================================
# Step 5 + Step 6: TF-IDF Vectorization & Skill Similarity
# =============================================

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# -----------------------
# 1️⃣ Load worker and job skill sentences
# -----------------------
worker_df = pd.read_csv("worker_skill_sentences.csv")  # columns: worker_id, skill_sentence
job_df = pd.read_csv("job_skill_sentences.csv")        # columns: job_id, skill_sentence

print(f"Workers loaded: {len(worker_df)}")
print(f"Jobs loaded: {len(job_df)}")

# -----------------------
# 2️⃣ TF-IDF Vectorization
# -----------------------
vectorizer = TfidfVectorizer()

# Fit on worker skills, transform workers
worker_vectors = vectorizer.fit_transform(worker_df["skill_sentence"])

# Transform jobs using the same vectorizer
job_vectors = vectorizer.transform(job_df["skill_sentence"])

print("TF-IDF vectorization complete.")
print(f"Worker vector shape: {worker_vectors.shape}")
print(f"Job vector shape: {job_vectors.shape}")

# Optional: Save vectors if needed
np.save("worker_vectors.npy", worker_vectors.toarray())
np.save("job_vectors.npy", job_vectors.toarray())

# -----------------------
# 3️⃣ Cosine Similarity Calculation
# -----------------------
# similarity_matrix[i,j] = similarity between worker i and job j
similarity_matrix = cosine_similarity(worker_vectors, job_vectors)
print("Cosine similarity matrix computed.")
print(f"Shape: {similarity_matrix.shape}")

# -----------------------
# 4️⃣ Create a long-format DataFrame
# -----------------------
similarity_list = []

for w_idx, worker_id in enumerate(worker_df["worker_id"]):
    for j_idx, job_id in enumerate(job_df["job_id"]):
        similarity_list.append({
            "worker_id": worker_id,
            "job_id": job_id,
            "skill_similarity": similarity_matrix[w_idx, j_idx]
        })

similarity_df = pd.DataFrame(similarity_list)

# -----------------------
# 5️⃣ Save to CSV
# -----------------------
similarity_df.to_csv("worker_job_similarity.csv", index=False)
print("worker_job_similarity.csv created successfully.")
print(similarity_df.head())