# ================================================
# Phase 2: Worker Clustering
# ================================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

# -----------------------
# 1️⃣ Set project directory
# -----------------------
PROJECT_DIR = r"D:\Projects\LNM_project"
os.chdir(PROJECT_DIR)
print("Working directory:", os.getcwd())

# -----------------------
# 2️⃣ Load worker skill embeddings
# -----------------------
skill_embeddings = np.load(r"D:\Projects\LNM_project\ml\pipelines\worker_vectors.npy")
print("Loaded skill embeddings:", skill_embeddings.shape)

# -----------------------
# 3️⃣ Load worker info
# -----------------------
workers_df = pd.read_csv(r"D:\Projects\LNM_project\ml\pipelines\workers_df.csv", dtype={"id": str})
worker_sent_df = pd.read_csv(r"D:\Projects\LNM_project\ml\pipelines\worker_skill_sentences.csv", dtype={"worker_id": str})

workers_df = workers_df.set_index("id").loc[worker_sent_df["worker_id"]].reset_index()
worker_ids = worker_sent_df["worker_id"].values

# 🔥 ADD THIS
if len(worker_ids) != skill_embeddings.shape[0]:
    raise ValueError("Mismatch between embeddings and worker IDs")

# Extract experience and total_jobs_done
features_numeric = workers_df[['experience_years','total_jobs_done']].values
print("Numeric features shape:", features_numeric.shape)

# -----------------------
# 4️⃣ Scale numeric features
# -----------------------
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features_numeric)

# -----------------------
# 5️⃣ Combine skill embeddings + numeric features
# -----------------------
X = np.hstack([skill_embeddings, features_scaled])
print("Combined feature matrix shape:", X.shape)

# -----------------------
# 6️⃣ Apply K-Means Clustering
# -----------------------
n_clusters = 5  # You can adjust this
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(X)

# -----------------------
# 7️⃣ Save cluster assignments
# -----------------------
cluster_df = pd.DataFrame({
    'worker_id': worker_ids,
    'cluster_id': cluster_labels
})

cluster_df.to_csv("worker_clusters.csv", index=False)
print("Worker clustering completed! Saved to worker_clusters.csv")
print(cluster_df.head())

# -----------------------
# ✅ Optional: Save KMeans and scaler for future use
# -----------------------
import pickle
with open("kmeans_model.pkl", "wb") as f:
    pickle.dump(kmeans, f)
with open("worker_scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
print("KMeans model and scaler saved for future use.")