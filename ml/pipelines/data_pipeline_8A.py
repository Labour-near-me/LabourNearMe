import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import pickle

print("Loading worker embeddings...")

# Load embeddings
worker_vectors = np.load("../vectors/worker_vectors.npy").astype(np.float64)

# Load worker ids
workers_df = pd.read_csv("workers_df.csv", dtype={"id": str})

print("Worker vectors shape:", worker_vectors.shape)
print("Workers loaded:", len(workers_df))


# -------------------------------------------------
# 1️⃣ Choose number of clusters
# -------------------------------------------------

# You can adjust this if needed
NUM_CLUSTERS = 8

print("Training KMeans clustering model...")

kmeans = KMeans(
    n_clusters=NUM_CLUSTERS,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(worker_vectors)

print("Clustering completed.")


# -------------------------------------------------
# 2️⃣ Build cluster dataset
# -------------------------------------------------

cluster_df = pd.DataFrame({
    "worker_id": workers_df["id"],
    "worker_cluster": clusters
})

print("Cluster distribution:")
print(cluster_df["worker_cluster"].value_counts())


# -------------------------------------------------
# 3️⃣ Save results
# -------------------------------------------------

cluster_df.to_csv("worker_clusters.csv", index=False)

with open("kmeans_model.pkl", "wb") as f:
    pickle.dump(kmeans, f)

print("Worker clusters saved successfully.")

print("Sample clusters:")
print(cluster_df.head())