# ==============================================
# Phase 2: Predictive Model Training
# ==============================================

import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------
# 1️⃣ Load ML-ready dataset
# -----------------------
df = pd.read_csv("ml_ready_dataset.csv")
print("Loaded dataset shape:", df.shape)

# -----------------------
# 2️⃣ Drop ID columns (not useful for learning)
# -----------------------
df = df.drop(columns=["worker_id", "job_id"])
print("Dropped worker_id and job_id")

# -----------------------
# 3️⃣ Separate features and target
# -----------------------
y = df["final_rating"]
X = df.drop(columns=["final_rating"])

print("Feature matrix shape:", X.shape)
print("Target shape:", y.shape)

# -----------------------
# 4️⃣ Convert any remaining categorical columns
# (If title/description are still raw text, drop them for now)
# -----------------------

# Check if title/description exist
for col in ["title", "description"]:
    if col in X.columns:
        print(f"Dropping text column: {col}")
        X = X.drop(columns=[col])

# Convert any object columns using get_dummies
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

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)

# -----------------------
# 6️⃣ Train RandomForest Regressor
# -----------------------
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
# 8️⃣ Save Model
# -----------------------
with open("predictive_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel saved as predictive_model.pkl 🎯")