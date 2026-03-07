import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle

print("Loading datasets...")

# -------------------------------------------------
# Load required files
# -------------------------------------------------

worker_vectors = np.load("../vectors/worker_vectors.npy").astype(np.float64)
workers_df = pd.read_csv("workers_df.csv", dtype={"id": str})
ml_df = pd.read_csv("predictive_training_dataset.csv", dtype={"worker_id": str})

print("Worker vectors:", worker_vectors.shape)
print("Workers:", workers_df.shape)
print("ML dataset:", ml_df.shape)

# -------------------------------------------------
# PIPELINE 8 — Worker Clustering
# -------------------------------------------------

print("\nTraining worker clustering model...")

NUM_CLUSTERS = 8

kmeans = KMeans(
    n_clusters=NUM_CLUSTERS,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(worker_vectors)

cluster_df = pd.DataFrame({
    "worker_id": workers_df["id"],
    "worker_cluster": clusters
})

print("Cluster distribution:")
print(cluster_df["worker_cluster"].value_counts())

# -------------------------------------------------
# PIPELINE 9 — Merge clusters with ML dataset
# -------------------------------------------------

print("\nMerging clusters with ML dataset...")

df = ml_df.merge(
    cluster_df,
    on="worker_id",
    how="left"
)

df["worker_cluster"] = df["worker_cluster"].fillna(-1).astype(int)

print("Dataset after merge:", df.shape)

# -------------------------------------------------
# Prepare training features
# -------------------------------------------------

print("\nPreparing training data...")

X = df.drop(columns=[
    "worker_id",
    "job_id",
    "title",
    "description",
    "final_rating"
])

y = df["final_rating"]

# Convert status to numeric
X = pd.get_dummies(X, columns=["status"])

print("Feature columns:", X.columns.tolist())

# -------------------------------------------------
# PIPELINE 10 — Train Predictive Model
# -------------------------------------------------

print("\nTraining predictive model...")

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

preds = model.predict(X)

rmse = np.sqrt(mean_squared_error(y, preds))

print("Training RMSE:", rmse)

# -------------------------------------------------
# Save artifacts
# -------------------------------------------------

print("\nSaving models...")

with open("predictive_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("kmeans_model.pkl", "wb") as f:
    pickle.dump(kmeans, f)

with open("feature_columns.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("Models saved successfully.")

print("\nPipeline completed.")