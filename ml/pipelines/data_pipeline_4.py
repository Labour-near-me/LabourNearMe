# =============================================
# Step 7: Build Predictive Training Dataset
# =============================================

import pandas as pd
import numpy as np

# -----------------------
# 1️⃣ Load required CSVs
# -----------------------
similarity_df = pd.read_csv("worker_job_similarity.csv")  # worker_id, job_id, skill_similarity
workers_df = pd.read_csv("workers_df.csv")               # id, created_at, experience_years, expected_wage, location_lat, location_lng, availability_status, rating, total_jobs_done
jobs_df = pd.read_csv("jobs_df.csv")                     # id, employer_id, title, description, budget, status, created_at, location_lat, location_lng
applications_df = pd.read_csv("applications_df.csv")     # id, job_id, worker_id, status, applied_at
ratings_df = pd.read_csv("ratings_df.csv")               # id, job_id, reviewer_id, reviewee_id, rating_value, feedback, created_at

print("All CSVs loaded.")

# -----------------------
# 2️⃣ Merge skill similarity with other features
# -----------------------
# Start with skill similarity
df = similarity_df.copy()

# Merge worker features
df = df.merge(
    workers_df[['id','experience_years','rating','location_lat','location_lng']], 
    left_on='worker_id', 
    right_on='id', 
    how='left'
)
df = df.rename(columns={'id':'worker_unique_id', 'location_lat':'worker_lat','location_lng':'worker_lng'})

# Merge job features
df = df.merge(
    jobs_df[['id','location_lat','location_lng','budget','status','title','description']], 
    left_on='job_id', 
    right_on='id', 
    how='left'
)
df = df.rename(columns={'id':'job_unique_id','location_lat':'job_lat','location_lng':'job_lng'})

# Merge application info (optional: filter only applied jobs)
df = df.merge(
    applications_df[['worker_id','job_id','status']], 
    on=['worker_id','job_id'], 
    how='left',
    suffixes=('', '_application')
)

# Merge final ratings (target variable)
df = df.merge(
    ratings_df[['reviewee_id','job_id','rating_value']], 
    left_on=['worker_id','job_id'], 
    right_on=['reviewee_id','job_id'], 
    how='left'
)
df = df.rename(columns={'rating_value':'final_rating'})

# -----------------------
# 3️⃣ Feature Engineering
# -----------------------
# 3a. Experience bucket
def experience_bucket(x):
    if x <= 2:
        return 0
    elif x <= 5:
        return 1
    else:
        return 2

df['experience_bucket'] = df['experience_years'].apply(experience_bucket)

# 3b. Worker rating normalization
df['avg_rating'] = df['rating']

# 3c. Distance calculation (if coordinates available)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(delta_lambda/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

df['distance_km'] = df.apply(lambda x: haversine(x['worker_lat'], x['worker_lng'], x['job_lat'], x['job_lng']), axis=1)

# -----------------------
# 4️⃣ Filter only rows with final rating (target)
# -----------------------
df_final = df[df['final_rating'].notnull()]

# -----------------------
# 5️⃣ Select final columns for ML
# -----------------------
ml_columns = [
    'worker_id', 'job_id', 'skill_similarity', 'experience_bucket',
    'avg_rating', 'distance_km', 'budget', 'status', 'title', 'description', 'final_rating'
]

df_ml = df_final[ml_columns]

# -----------------------
# 6️⃣ Save predictive training dataset
# -----------------------
df_ml.to_csv("predictive_training_dataset.csv", index=False)
print("predictive_training_dataset.csv created successfully!")
print(df_ml.head())