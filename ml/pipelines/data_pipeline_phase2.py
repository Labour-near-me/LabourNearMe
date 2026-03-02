# ==============================================
# Phase 2: Predictive Model Training
# ==============================================

import pandas as pd
import numpy as np
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------
# 1️⃣ Load ML-ready dataset (Updated Path)
# -----------------------
# Navigates from ml/pipelines/ to data/processed/
DATA_PATH = os.path.join("..", "..", "data", "processed", "ml_ready_dataset.csv")

if not os.path.exists(DATA_PATH):
    print(f"❌ Error: Could not find dataset at {DATA_PATH}")
    print("Ensure you are running this script from inside: LabourNearMe/ml/pipelines/")
    exit()

df = pd.read_csv(DATA_PATH)
print("Loaded dataset shape:", df.shape)

# -----------------------
# 2️⃣ Drop ID columns
# -----------------------
# Standard cleanup for the LabourLink model
cols_to_drop = ["worker_id", "job_id"]
df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
print(f"Dropped ID columns. New shape: {df.shape}")

# -----------------------
# 3️⃣ Separate features and target
# -----------------------
# Ensuring the target 'final_rating' exists from your Phase 1 processing
if "final_rating" not in df.columns:
    print("❌ Error: 'final_rating' column missing. Check your Phase 1 output.")
    exit()

y = df["final_rating"]
X = df.drop(columns=["final_rating"])

# -----------------------
# 4️⃣ Preprocessing & Encoding
# -----------------------
# Dropping raw text before encoding for the Random Forest model
for col in ["title", "description"]:
    if col in X.columns:
        print(f"Dropping text column: {col}")
        X = X.drop(columns=[col])

# Convert categorical columns (location, job_type) to numeric
X = pd.get_dummies(X, drop_first=True)
print("Final feature matrix shape after encoding:", X.shape)

# -----------------------
# 5️⃣ Train/Test Split
# -----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# -----------------------
# 6️⃣ Train RandomForest Regressor
# -----------------------
# Using 200 estimators for better stability in worker matching
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)
print("Model training completed ✅")

# -----------------------
# 7️⃣ Evaluate Model
# -----------------------
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n📊 Model Performance:")
print("MAE :", round(mae, 4))
print("RMSE:", round(rmse, 4))
print("R²  :", round(r2, 4))

# -----------------------
# 8️⃣ Save Model + Feature Columns (Updated Path)
# -----------------------
# Saving to ml/models/ folder for Phase 3 use
MODEL_DIR = os.path.join("..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

with open(os.path.join(MODEL_DIR, "predictive_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(MODEL_DIR, "feature_columns.pkl"), "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print(f"\nModel and feature columns saved to {MODEL_DIR} 🎯")