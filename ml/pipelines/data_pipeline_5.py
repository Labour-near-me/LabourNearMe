# =========================================
# Phase 1 Final Prep: Scaling, Encoding & Train/Test Split
# =========================================

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import pickle

# -----------------------
# 1️⃣ Load predictive dataset
# -----------------------
df = pd.read_csv("predictive_training_dataset.csv")
print("Loaded predictive dataset:", df.shape)

# -----------------------
# 2️⃣ Scale numeric features
# -----------------------
numeric_cols = ['skill_similarity', 'experience_bucket', 'avg_rating', 'distance_km', 'budget']

scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Save scaler
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Numeric features scaled:", numeric_cols)

# -----------------------
# 3️⃣ Encode categorical features
# -----------------------
categorical_cols = ['status']  # add 'title', 'description' if needed

# Fix for newer sklearn versions
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_data = encoder.fit_transform(df[categorical_cols])

encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_cols))
df = pd.concat([df.drop(columns=categorical_cols), encoded_df], axis=1)

# Save encoder
with open("encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Categorical features encoded:", categorical_cols)

# -----------------------
# 4️⃣ Split into Train/Test sets
# -----------------------
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save to CSV
train_df.to_csv("train_dataset.csv", index=False)
test_df.to_csv("test_dataset.csv", index=False)

print("Train/Test split done:")
print("Train:", train_df.shape)
print("Test:", test_df.shape)

# -----------------------
# ✅ Phase 1 complete
# -----------------------
print("Phase 1 ML-ready dataset is ready!")