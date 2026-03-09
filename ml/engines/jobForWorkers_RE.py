import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from ml.engines.model_validator import predict_score
from ml.engines.workerForJob_RE import (
    WORKERS_DF,
    JOBS_DF,
    WORKER_VEC,
    JOB_VEC,
    WORKER_SKILLS_DF,
    JOB_SKILLS_DF,
    haversine,
    kmeans
)

SIMILARITY_THRESHOLD = 0.45
MAX_DISTANCE_KM = 20


def recommend_jobs_for_worker(worker_id, top_n=5):

    worker_index = WORKERS_DF.index[WORKERS_DF["id"] == worker_id][0]

    worker_row = WORKERS_DF.iloc[worker_index]

    worker_vector = WORKER_VEC[worker_index].reshape(1, -1)

    similarities = cosine_similarity(worker_vector, JOB_VEC)[0]

    # -----------------------------------
    # GET WORKER SKILLS
    # -----------------------------------

    worker_skills = set(
        WORKER_SKILLS_DF[
            WORKER_SKILLS_DF["worker_id"] == worker_id
        ]["skill_id"]
    )

    results = []

    for i, job in JOBS_DF.iterrows():

        # -----------------------------------
        # GET JOB SKILLS
        # -----------------------------------

        job_skills = set(
            JOB_SKILLS_DF[
                JOB_SKILLS_DF["job_id"] == job["id"]
            ]["skill_id"]
        )

        # -----------------------------------
        # SKILL MATCHING
        # -----------------------------------

        matched_skills = len(worker_skills & job_skills)

        if matched_skills == 0:
            continue

        similarity = similarities[i]

        if similarity < SIMILARITY_THRESHOLD:
            continue

        # -----------------------------------
        # DISTANCE CALCULATION
        # -----------------------------------

        distance = haversine(
            worker_row["location_lat"],
            worker_row["location_lng"],
            job["location_lat"],
            job["location_lng"]
        )

        if distance > MAX_DISTANCE_KM:
            continue

        # -----------------------------------
        # EXPERIENCE BUCKET
        # -----------------------------------

        experience_bucket = 0
        if worker_row["experience_years"] > 5:
            experience_bucket = 2
        elif worker_row["experience_years"] > 2:
            experience_bucket = 1

        # -----------------------------------
        # WORKER CLUSTER
        # -----------------------------------

        vector = np.array(WORKER_VEC[worker_index], dtype=np.float64).reshape(1, -1)
        worker_cluster = int(kmeans.predict(vector)[0])

        # -----------------------------------
        # MODEL FEATURES
        # -----------------------------------

        features = pd.DataFrame([{
            "skill_similarity": similarity,
            "experience_bucket": experience_bucket,
            "avg_rating": worker_row["rating"],
            "distance_km": distance,
            "budget": job["budget"],
            "status": job["status"],
            "worker_cluster": worker_cluster
        }])

        predictive_score = float(predict_score(features)) / 5

        # -----------------------------------
        # SCORING COMPONENTS
        # -----------------------------------

        rating_score = worker_row["rating"] / 5
        proximity_score = 1 / (1 + distance)

        skill_boost = matched_skills / max(len(job_skills), 1)

        # -----------------------------------
        # FINAL SCORE
        # -----------------------------------

        final_score = (
            0.35 * similarity +
            0.20 * rating_score +
            0.20 * proximity_score +
            0.15 * predictive_score +
            0.10 * skill_boost
        )

        results.append({
            "job_id": job["id"],
            "title": job["title"],
            "score": round(float(final_score), 3),
            "distance_km": round(float(distance), 3),
            "similarity": round(float(similarity), 3),
            "predictive_score": round(float(predictive_score), 3),
            "matched_skills": matched_skills
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:top_n]

if __name__ == "__main__":
    print("\nTesting recommendation engine with random samples...\n")

    # Pick random workers to test instead of random jobs
    test_workers = WORKERS_DF["id"].sample(3).tolist() 

    for worker_id in test_workers:
        print(f"\n--- Recommended jobs for worker: {worker_id} ---")

        # FIX: Ensure this name matches the function defined at the top of THIS file
        results = recommend_jobs_for_worker(worker_id, top_n=5)

        for r in results:
            print(r)