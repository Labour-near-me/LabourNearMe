# ==============================================
# prepare_ml_dataset.py
# Merge Worker Clusters into Predictive Dataset
# Fully ML-ready CSV for model training
# ==============================================

import pandas as pd

# -----------------------
# 1️⃣ Load existing datasets
# -----------------------
predictive_df = pd.read_csv("predictive_training_dataset.csv")  # predictive dataset
worker_clusters = pd.read_csv("worker_clusters.csv")            # worker_id, cluster_id

print("Predictive dataset loaded:", predictive_df.shape)
print("Worker clusters loaded:", worker_clusters.shape)

# -----------------------
# 2️⃣ Merge cluster_id into predictive dataset
# -----------------------
df_ml_ready = predictive_df.merge(worker_clusters, on="worker_id", how="left")

# -----------------------
# 3️⃣ Optional: Check for any missing cluster_ids
# -----------------------
missing_clusters = df_ml_ready['cluster_id'].isnull().sum()
if missing_clusters > 0:
    print(f"⚠️ Warning: {missing_clusters} rows missing cluster_id. Filling with -1")
    df_ml_ready['cluster_id'] = df_ml_ready['cluster_id'].fillna(-1).astype(int)
else:
    print("All workers have cluster_id assigned ✅")

# -----------------------
# 4️⃣ Save fully ML-ready CSV
# -----------------------
output_file = "ml_ready_dataset.csv"
df_ml_ready.to_csv(output_file, index=False)
print(f"Fully ML-ready dataset saved to {output_file}")
print(df_ml_ready.head())

# -----------------------
# 5️⃣ Summary
# -----------------------
print(f"Final dataset shape: {df_ml_ready.shape}")
print(f"Columns: {list(df_ml_ready.columns)}")