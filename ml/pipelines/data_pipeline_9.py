"""
ml/pipelines/data_pipeline_9.py  (FIXED VERSION)
-------------------------------------------------
Bug fixed vs original:
  - predictive_training_dataset.csv has EXACTLY ONE status value in it:
    'completed' (verified: every row's status column == 'completed',
    which makes sense because final_rating only exists after a job is
    marked completed). The model was trained with a one-hot 'status'
    feature that therefore had zero variance.
  - At inference time (jobForWorkers_RE.py / workerForJob_RE.py) the
    engines score jobs with status = 'open' — a category the model
    NEVER saw during training. This is a genuine train/serve skew and
    silently distorts ml_score, which carries 60% of final_score.

  FIX: drop 'status' entirely from the feature set. It carries no
  learnable signal (constant in training data) and only introduces
  out-of-distribution risk at inference. If job lifecycle stage is
  ever wanted as a signal in the future, it needs to be re-collected
  across ALL statuses (open/assigned/completed/cancelled), not just
  completed ones, before being reintroduced as a feature.
"""

import pickle

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

print("Loading datasets...")

worker_vectors = np.load(r"E:\appu\Desktop\LNMproject_Upgraded\labournearme\ml\pipelines\worker_vectors.npy").astype(np.float64)

workers_df = pd.read_csv(
    r"E:\appu\Desktop\LNMproject_Upgraded\labournearme\ml\pipelines\workers_df.csv",
    dtype={"id": str}
)

worker_sent_df = pd.read_csv(
    r"E:\appu\Desktop\LNMproject_Upgraded\labournearme\ml\pipelines\worker_skill_sentences.csv",
    dtype={"worker_id": str}
)

ml_df = pd.read_csv(
    r"E:\appu\Desktop\LNMproject_Upgraded\labournearme\ml\pipelines\predictive_training_dataset.csv",
    dtype={"worker_id": str}
)

print("Worker vectors:", worker_vectors.shape)
print("Workers:", workers_df.shape)
print("ML dataset:", ml_df.shape)

# Sanity check: warn loudly if status ever stops being constant, since that
# changes whether it's safe to drop.
unique_statuses = ml_df["status"].unique().tolist() if "status" in ml_df.columns else []
print("Unique status values found in training data:", unique_statuses)

# -------------------------------------------------
# Worker Clustering
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
    "worker_id": worker_sent_df["worker_id"],
    "worker_cluster": clusters
})

print("Cluster distribution:")
print(cluster_df["worker_cluster"].value_counts())

# -------------------------------------------------
# Merge clusters with ML dataset
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

# FIX: 'status' dropped — it was constant ('completed') across every
# training row, so its one-hot columns contributed no signal, and at
# inference time the engines score 'open' jobs, a category the model
# never saw. Keeping it created a silent train/serve mismatch.
X = df.drop(columns=[
    "worker_id",
    "job_id",
    "title",
    "description",
    "final_rating",
    "status",          # <-- FIX: removed
], errors="ignore")

y = df["final_rating"]

print("Feature columns:", X.columns.tolist())

# -------------------------------------------------
# Train/Test Split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -------------------------------------------------
# Train Predictive Model
# -------------------------------------------------

print("\nTraining predictive model...")

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, preds))

print("Test RMSE:", rmse)

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
print("NOTE: feature_columns.pkl no longer contains any status_* columns.")
print("Re-deploy predictive_model.pkl, kmeans_model.pkl, and feature_columns.pkl")
print("together to backend/ml/models/ — the three files must always match.")

print("\nPipeline completed.")