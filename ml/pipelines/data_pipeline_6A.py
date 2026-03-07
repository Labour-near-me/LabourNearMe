import pandas as pd
import numpy as np

print("Loading datasets...")

similarity_df = pd.read_csv("worker_job_similarity.csv", dtype={"worker_id": str, "job_id": str})
workers_df = pd.read_csv("workers_df.csv", dtype={"id": str})
jobs_df = pd.read_csv("jobs_df.csv", dtype={"id": str})
ratings_df = pd.read_csv("ratings_df.csv", dtype={"reviewee_id": str, "job_id": str})

print("Datasets loaded.")

# -------------------------------------------------
# Start from ratings (target data)
# -------------------------------------------------

df = ratings_df.copy()

df = df.rename(columns={
    "reviewee_id": "worker_id",
    "rating_value": "final_rating"
})

# -------------------------------------------------
# Merge similarity feature
# -------------------------------------------------

df = df.merge(
    similarity_df,
    on=["worker_id", "job_id"],
    how="left"
)

df["skill_similarity"] = df["skill_similarity"].fillna(0)

# -------------------------------------------------
# Merge worker features
# -------------------------------------------------

df = df.merge(
    workers_df[['id','experience_years','rating','location_lat','location_lng']],
    left_on='worker_id',
    right_on='id',
    how='left'
)

df.rename(columns={
    "location_lat":"worker_lat",
    "location_lng":"worker_lng"
}, inplace=True)

df.drop(columns=["id"], inplace=True, errors="ignore")

# -------------------------------------------------
# Merge job features
# -------------------------------------------------

df = df.merge(
    jobs_df[['id','location_lat','location_lng','budget','status','title','description']],
    left_on="job_id",
    right_on="id",
    how="left"
)

df.rename(columns={
    "location_lat":"job_lat",
    "location_lng":"job_lng"
}, inplace=True)

df.drop(columns=["id"], inplace=True, errors="ignore")

# -------------------------------------------------
# Feature engineering
# -------------------------------------------------

def experience_bucket(x):
    if x <= 2:
        return 0
    elif x <= 5:
        return 1
    else:
        return 2

df["experience_bucket"] = df["experience_years"].fillna(0).apply(experience_bucket)

df["avg_rating"] = df["rating"].fillna(0)

# -------------------------------------------------
# Distance calculation
# -------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians,[lat1,lon1,lat2,lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2*np.arcsin(np.sqrt(a))
    return R*c

df["distance_km"] = df.apply(
    lambda x: haversine(x["worker_lat"],x["worker_lng"],x["job_lat"],x["job_lng"]),
    axis=1
)

# -------------------------------------------------
# Final ML dataset
# -------------------------------------------------

ml_columns = [
    "worker_id",
    "job_id",
    "skill_similarity",
    "experience_bucket",
    "avg_rating",
    "distance_km",
    "budget",
    "status",
    "title",
    "description",
    "final_rating"
]

df_ml = df[ml_columns]

df_ml.to_csv("predictive_training_dataset.csv", index=False)

print("predictive_training_dataset.csv created successfully")
print("Dataset shape:", df_ml.shape)
print(df_ml.head())