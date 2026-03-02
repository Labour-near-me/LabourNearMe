import os
import time
import logging
import joblib
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from sklearn.metrics.pairwise import cosine_similarity

# ===============================
# 1. SETUP CACHE & ASSETS
# ===============================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data")
VECTOR_DIR = os.path.join(BASE_DIR, "..", "vectors")

try:
    # Using Precomputed Vectors for speed
    WORKER_VEC = np.load(os.path.join(VECTOR_DIR, "worker_vectors.npy"))
    JOB_VEC = np.load(os.path.join(VECTOR_DIR, "job_vectors.npy"))
    
    # Load ML Model and Alignment Blueprint
    MODEL = joblib.load(os.path.join(MODEL_DIR, "predictive_model.pkl"))
    FEATURE_COLS = joblib.load(os.path.join(MODEL_DIR, "feature_columns.pkl"))
    
    # Load Core Dataframes
    WORKERS_DF = pd.read_csv(os.path.join(DATA_DIR, "raw", "workers_df.csv"))
    JOBS_DF = pd.read_csv(os.path.join(DATA_DIR, "raw", "jobs_df.csv"))
    WORKER_CLUSTERS = pd.read_csv(os.path.join(DATA_DIR, "processed", "worker_clusters.csv"))
    
    logger.info("✅ Assets Loaded: System ready for high-speed strict inference.")
except Exception as e:
    logger.error(f"❌ Startup Error: {e}")
    raise

# ===============================
# 2. THE PRODUCTION ENGINE
# ===============================
def recommend_workers_for_job(job_id, top_n=5):
    """
    Ranks workers for a specific job based on:
    1. Mandatory Skill Similarity > 0
    2. Geographic Proximity (Haversine)
    3. ML-based predicted success rating
    """
    start_time = time.time()
    
    # 1. Validation: Find Job Index
    job_indices = JOBS_DF.index[JOBS_DF['id'] == job_id].tolist()
    if not job_indices:
        return {"error": "Job not found", "status": 404}
    
    job_idx = job_indices[0]
    job = JOBS_DF.iloc[job_idx]

    # 2. Vectorized Skill Similarity Calculation
    # Reshaping job vector for cosine_similarity
    target_job_vector = JOB_VEC[job_idx].reshape(1, -1)
    similarities = cosine_similarity(target_job_vector, WORKER_VEC)[0]

    # 3. Data Merging & STRICT FILTERING
    # Merge workers with their clusters
    candidates = WORKERS_DF.merge(WORKER_CLUSTERS, left_on="id", right_on="worker_id")
    candidates["skill_similarity"] = similarities

    # --- CRITICAL FILTER: ONLY WORKERS WITH RELEVANT SKILLS ---
    candidates = candidates[candidates["skill_similarity"] > 0].copy()
    
    if candidates.empty:
        logger.warning(f"No workers found with matching skills for job {job_id}")
        return []

    # 4. Distance calculation (Haversine Vectorized)
    def hv(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        d = np.sin((lat2-lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2-lon1)/2)**2
        return 2 * 6371 * np.arcsin(np.sqrt(d))

    candidates["distance_km"] = hv(job["location_lat"], job["location_lng"], 
                                   candidates["location_lat"], candidates["location_lng"])

    # 5. ML-BASED SCORING
    # Preparing data to match model training format
    input_data = pd.DataFrame({
        "skill_similarity": candidates["skill_similarity"],
        "experience_bucket": candidates["experience_years"].apply(lambda x: 0 if x<=2 else 1 if x<=5 else 2),
        "avg_rating": candidates["rating"],
        "distance_km": candidates["distance_km"],
        "budget": job["budget"],
        "status": "completed",
        "cluster_id": candidates["cluster_id"]
    })
    
    # Align features (One-hot encoding and reindexing)
    X = pd.get_dummies(input_data).reindex(columns=FEATURE_COLS, fill_value=0)
    
    # Predict the score
    candidates["final_score"] = MODEL.predict(X)

    # 6. Tie-Breaker Logic
    # Prioritizes workers who actually match the skills better if ratings are equal
    candidates["final_score"] += (candidates["skill_similarity"] * 0.01)

    # 7. Final Selection
    results = candidates.sort_values(by="final_score", ascending=False).head(top_n)
    
    execution_time = time.time() - start_time
    logger.info(f"⚡ Strict Ranking completed in {execution_time:.4f} seconds")
    
    return results[["id", "final_score", "distance_km", "skill_similarity", "rating"]].to_dict(orient="records")

# ===============================
# 3. CLI TEST BLOCK
# ===============================
if __name__ == "__main__":
    # Test Job ID provided by user
    sample_job_id = "1946d24e-c1cf-453c-9171-ab75765d1405"
    
    print(f"\n🔍 Running Strict Ranking for Job: {sample_job_id}")
    workers = recommend_workers_for_job(sample_job_id, top_n=5)
    
    print("="*85)
    if isinstance(workers, list) and len(workers) > 0:
        for w in workers:
            print(f"Worker: {w['id']} | Score: {w['final_score']:.4f} | Similarity: {w['skill_similarity']:.2f} | Dist: {w['distance_km']:.2f}km | Rating: {w['rating']}")
    elif isinstance(workers, list) and len(workers) == 0:
        print("No workers matched the required skills.")
    else:
        print(f"Error: {workers}")
    print("="*85)