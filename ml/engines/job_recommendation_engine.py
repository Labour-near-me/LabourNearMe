import os
import ast
import logging
import numpy as np
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------
# LOGGING
# -------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# LOAD ENV & DATABASE
# -------------------------------------------------
load_dotenv()
db_url = os.getenv("DATABASE_URL")
if not db_url:
    logger.error("DATABASE_URL not found in .env file!")
    exit(1)

engine = create_engine(db_url)

# -------------------------------------------------
# LOAD DATA FROM DATABASE
# -------------------------------------------------
def load_data():
    logger.info("Loading workers and jobs from DATABASE...")

    # Fetch data - Note: 'Jobs' is case-sensitive in your DB
    workers_df = pd.read_sql("SELECT * FROM workers", engine)
    jobs_df = pd.read_sql('SELECT * FROM "Jobs"', engine)

    # Convert UUID to string for matching
    workers_df["id"] = workers_df["id"].astype(str)
    jobs_df["id"] = jobs_df["id"].astype(str)

    return workers_df, jobs_df


# -------------------------------------------------
# CONVERT EMBEDDINGS FROM STRING/LIST → NUMPY ARRAY
# -------------------------------------------------
def convert_embeddings(df, column_name):
    vectors = []
    for v in df[column_name]:
        if isinstance(v, str):
            # If database returns vector as a string "[1, 2, 3...]"
            vectors.append(np.array(ast.literal_eval(v), dtype=float))
        elif isinstance(v, list):
            # If driver already converted it to a list
            vectors.append(np.array(v, dtype=float))
        else:
            # Handle unexpected types (like None)
            vectors.append(np.zeros(143)) # Default to zero vector if empty
            
    return np.array(vectors)


# -------------------------------------------------
# HAVERSINE DISTANCE (KM)
# -------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


# -------------------------------------------------
# MAIN RECOMMENDATION FUNCTION
# -------------------------------------------------
def recommend_workers_for_job(job_id, top_n=5):

    if job_id not in JOBS_DF["id"].values:
        return {"error": "Job not found", "status": 404}

    # Get job index
    job_index = JOBS_DF.index[JOBS_DF["id"] == job_id][0]
    job_row = JOBS_DF.iloc[job_index]

    target_job_vector = JOB_VEC[job_index].reshape(1, -1)

    # Cosine similarity
    similarities = cosine_similarity(target_job_vector, WORKER_VEC)[0]

    results = []

    for i, worker in WORKERS_DF.iterrows():
        similarity_score = similarities[i]

        # Strict Skill Filtering (threshold)
        if similarity_score < 0.30:
            continue

        # Distance Calculation using correct column names from your DB
        distance_km = haversine(
            worker["location_lat"],
            worker["location_lng"],
            job_row["location_lat"],
            job_row["location_lng"]
        )

        # Final scoring logic (Weights: 60% Skills, 20% Proximity, 20% Rating)
        # We normalize rating by 5 assuming it's a 5-star system
        rating_score = (worker["rating"] / 5.0) if pd.notnull(worker["rating"]) else 0
        proximity_score = 1 / (1 + distance_km)

        final_score = (
            0.6 * similarity_score +
            0.2 * proximity_score +
            0.2 * rating_score
        )

        results.append({
            "id": worker["id"],
            "skill_similarity": float(similarity_score),
            "distance_km": float(distance_km),
            "rating": worker["rating"],
            "final_score": float(final_score)
        })

    if not results:
        return []

    # Sort descending by final_score
    results = sorted(results, key=lambda x: x["final_score"], reverse=True)

    return results[:top_n]


# -------------------------------------------------
# INITIAL LOAD
# -------------------------------------------------
try:
    WORKERS_DF, JOBS_DF = load_data()

    WORKER_VEC = convert_embeddings(WORKERS_DF, "worker_embedding")
    JOB_VEC = convert_embeddings(JOBS_DF, "job_embedding")

    logger.info(f"✅ Assets Loaded. Workers: {len(WORKERS_DF)}, Jobs: {len(JOBS_DF)}")
except Exception as e:
    logger.error(f"❌ Failed to load data from database: {e}")
    exit(1)


# -------------------------------------------------
# TEST BLOCK
# -------------------------------------------------
if __name__ == "__main__":
    if not JOBS_DF.empty:
        sample_job_id = JOBS_DF["id"].iloc[0]

        print(f"\n🔍 Running Strict Ranking for Job ID: {sample_job_id}")
        print(f"Job Title: {JOBS_DF.iloc[0]['title']}")

        workers = recommend_workers_for_job(sample_job_id, top_n=5)

        print("="*90)
        if isinstance(workers, list) and len(workers) > 0:
            for w in workers:
                print(
                    f"Worker: {w['id']} | "
                    f"Final Score: {w['final_score']:.4f} | "
                    f"Similarity: {w['skill_similarity']:.2f} | "
                    f"Dist: {w['distance_km']:.2f}km | "
                    f"Rating: {w['rating']}"
                )
        elif isinstance(workers, list) and len(workers) == 0:
            print("No workers matched the required skills (Similarity < 0.30).")
        else:
            print(f"Error: {workers}")
        print("="*90)
    else:
        print("No jobs found in database to test.")