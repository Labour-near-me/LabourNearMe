import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import pickle

print("Loading predictive dataset...")

df = pd.read_csv("predictive_training_dataset.csv")

print("Dataset shape:", df.shape)

# -------------------------------------------------
# 1️⃣ Separate target variable
# -------------------------------------------------

if "final_rating" not in df.columns:
    raise Exception("final_rating column missing!")

y = df["final_rating"]
X = df.drop(columns=["final_rating"])

# -------------------------------------------------
# 2️⃣ Scale numeric features
# -------------------------------------------------

numeric_cols = [
    "skill_similarity",
    "experience_bucket",
    "avg_rating",
    "distance_km",
    "budget"
]

scaler = StandardScaler()

X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

# Save scaler
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Numeric features scaled.")

# -------------------------------------------------
# 3️⃣ Encode categorical features
# -------------------------------------------------

categorical_cols = ["status"]

encoder = OneHotEncoder(
    sparse_output=False,
    handle_unknown="ignore"
)

encoded = encoder.fit_transform(X[categorical_cols])

encoded_df = pd.DataFrame(
    encoded,
    columns=encoder.get_feature_names_out(categorical_cols)
)

# Reset indexes before concat
X = X.reset_index(drop=True)
encoded_df = encoded_df.reset_index(drop=True)

X = pd.concat([X.drop(columns=categorical_cols), encoded_df], axis=1)

# Save encoder
with open("encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Categorical features encoded.")

# -------------------------------------------------
# 4️⃣ Train/Test Split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

train_df = pd.concat([X_train, y_train], axis=1)
test_df = pd.concat([X_test, y_test], axis=1)

train_df.to_csv("train_dataset.csv", index=False)
test_df.to_csv("test_dataset.csv", index=False)

print("Train/Test split completed.")

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)

print("Pipeline 7 completed successfully.")