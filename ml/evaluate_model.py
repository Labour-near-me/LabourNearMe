import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# ===============================
# 1. Path Configuration
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "predictive_model.pkl")
FEATURE_COLS_PATH = os.path.join(BASE_DIR, "models", "feature_columns.pkl")
TRAINING_DATA_PATH = os.path.join(BASE_DIR, "../data/processed/predictive_training_dataset.csv")
CLUSTER_DATA_PATH = os.path.join(BASE_DIR, "../data/processed/worker_clusters.csv")

# ===============================
# 2. Data Loading & REAL MERGE
# ===============================
try:
    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURE_COLS_PATH)
    
    # Load the datasets
    df = pd.read_csv(TRAINING_DATA_PATH)
    clusters_df = pd.read_csv(CLUSTER_DATA_PATH)

    # 🛠️ IMPROVEMENT: Instead of default (1), we perform a left-join on worker_id
    # This brings in the ACTUAL cluster_id for every worker in the training set
    if 'worker_id' in df.columns and 'worker_id' in clusters_df.columns:
        df = df.merge(clusters_df[['worker_id', 'cluster_id']], on='worker_id', how='left')
        # Fill only the ones that truly don't exist in the cluster file (fallback)
        df['cluster_id'] = df['cluster_id'].fillna(df['cluster_id'].mode()[0]) 
        print("✅ Successfully merged REAL cluster_ids from worker_clusters.csv")
    else:
        print("⚠️ Warning: Could not find worker_id in one of the files. Using mode.")
        df['cluster_id'] = 1 # Absolute fallback

    print("✅ Assets loaded and data aligned.")
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

# ===============================
# 3. Feature Selection & Alignment
# ===============================
raw_features = ["skill_similarity", "experience_bucket", "avg_rating", "distance_km", "budget", "cluster_id"]
y = df["final_rating"] if "final_rating" in df.columns else df["avg_rating"]

X_raw = df[raw_features]
X_processed = pd.get_dummies(X_raw)
X_final = X_processed.reindex(columns=feature_columns, fill_value=0)

X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# ===============================
# 4. Predict & Evaluate
# ===============================
try:
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\n📊 Truth-Based Evaluation Results")
    print("-" * 35)
    print(f"MAE  : {mae:.4f}")
    print(f"R²   : {r2:.4f}")

    # Show Importance to see if cluster_id actually moves the needle now
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        feat_names = X_final.columns
        print("\n🔍 Feature Importance (Real Data)")
        for i in np.argsort(importances)[::-1][:5]:
            print(f"{feat_names[i]:<20}: {importances[i]:.4f}")

except Exception as e:
    print(f"❌ Prediction failed: {e}")