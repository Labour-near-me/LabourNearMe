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

    workers_df = pd.read_sql("SELECT * FROM workers", engine)
    jobs_df = pd.read_sql('SELECT * FROM "Jobs"', engine)

    workers_df["id"] = workers_df["id"].astype(str)
    jobs_df["id"] = jobs_df["id"].astype(str)

    return workers_df, jobs_df


# -------------------------------------------------
# CONVERT EMBEDDINGS
# -------------------------------------------------
def convert_embeddings(df, column_name):
    vectors = []
    for v in df[column_name]:
        if isinstance(v, str):
            vectors.append(np.array(ast.literal_eval(v), dtype=float))
        elif isinstance(v, list):
            vectors.append(np.array(v, dtype=float))
        else:
            # Change this from 143 to 425
            vectors.append(np.zeros(425))            
    return np.array(vectors)

# -------------------------------------------------
# HAVERSINE DISTANCE
# -------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    lat1, lon1, lat2, lon2 = map(
        np.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2

    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


# -------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------
def recommend_jobs_for_worker(worker_id, top_n=5):

    if worker_id not in WORKERS_DF["id"].values:
        return {"error": "Worker not found", "status": 404}

    worker_index = WORKERS_DF.index[WORKERS_DF["id"] == worker_id][0]

    worker_row = WORKERS_DF.iloc[worker_index]

    target_worker_vector = WORKER_VEC[worker_index].reshape(1, -1)

    similarities = cosine_similarity(target_worker_vector, JOB_VEC)[0]

    results = []

    for i, job in JOBS_DF.iterrows():

        similarity_score = similarities[i]

        if similarity_score < 0.30:
            continue

        distance_km = haversine(
            worker_row["location_lat"],
            worker_row["location_lng"],
            job["location_lat"],
            job["location_lng"]
        )

        proximity_score = 1 / (1 + distance_km)

        budget_score = job["budget"] / 2000  # normalization

        final_score = (
            0.7 * similarity_score +
            0.15 * proximity_score +
            0.15 * budget_score
        )

        results.append({
            "id": job["id"],
            "title": job["title"],
            "similarity": float(similarity_score),
            "distance_km": float(distance_km),
            "budget": job["budget"],
            "final_score": float(final_score)
        })

    if not results:
        return []

    results = sorted(results, key=lambda x: x["final_score"], reverse=True)

    return results[:top_n]


# -------------------------------------------------
# INITIAL LOAD
# -------------------------------------------------
try:

    WORKERS_DF, JOBS_DF = load_data()

    WORKER_VEC = convert_embeddings(WORKERS_DF, "worker_embedding")
    JOB_VEC = convert_embeddings(JOBS_DF, "job_embedding")

    logger.info(
        f"✅ Assets Loaded. Workers: {len(WORKERS_DF)}, Jobs: {len(JOBS_DF)}"
    )

except Exception as e:

    logger.error(f"❌ Failed to load data from database: {e}")
    exit(1)


# -------------------------------------------------
# TEST BLOCK
# -------------------------------------------------
if __name__ == "__main__":

    if not WORKERS_DF.empty:

        sample_worker_id = WORKERS_DF["id"].iloc[0]

        print(f"\n🔍 Running Job Recommendation for Worker: {sample_worker_id}")

        jobs = recommend_jobs_for_worker(sample_worker_id, top_n=5)

        print("="*90)

        if isinstance(jobs, list) and len(jobs) > 0:

            for j in jobs:

                print(
                    f"Job: {j['title']} | "
                    f"Score: {j['final_score']:.4f} | "
                    f"Similarity: {j['similarity']:.2f} | "
                    f"Distance: {j['distance_km']:.2f}km | "
                    f"Budget: ₹{j['budget']}"
                )

        elif isinstance(jobs, list) and len(jobs) == 0:
            print("No jobs matched worker skills.")

        else:
            print(f"Error: {jobs}")

        print("="*90)

    else:
        print("No workers found in database to test.")