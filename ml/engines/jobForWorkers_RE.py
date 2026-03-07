import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from ml.engines.model_validator import predict_score
from ml.engines.workerForJob_RE import (
    WORKERS_DF,
    JOBS_DF,
    WORKER_VEC,
    JOB_VEC,
    haversine,
    kmeans
)

# -------------------------------------------------
# RECOMMEND JOBS FOR A WORKER
# -------------------------------------------------

def recommend_jobs_for_worker(worker_id, top_n=5):

    worker_index = WORKERS_DF.index[WORKERS_DF["id"] == worker_id][0]

    worker_row = WORKERS_DF.iloc[worker_index]

    worker_vector = WORKER_VEC[worker_index].reshape(1, -1)

    similarities = cosine_similarity(worker_vector, JOB_VEC)[0]

    results = []

    for i, job in JOBS_DF.iterrows():

        similarity = similarities[i]

        if similarity < 0.30:
            continue

        distance = haversine(
            worker_row["location_lat"],
            worker_row["location_lng"],
            job["location_lat"],
            job["location_lng"]
        )

        experience_bucket = 0
        if worker_row["experience_years"] > 5:
            experience_bucket = 2
        elif worker_row["experience_years"] > 2:
            experience_bucket = 1

        vector = np.array(WORKER_VEC[worker_index], dtype=np.float64).reshape(1, -1)
        worker_cluster = int(kmeans.predict(vector)[0])

        features = pd.DataFrame([{
            "skill_similarity": similarity,
            "experience_bucket": experience_bucket,
            "avg_rating": worker_row["rating"],
            "distance_km": distance,
            "budget": job["budget"],
            "status": job["status"],
            "worker_cluster": worker_cluster
        }])

        score = predict_score(features)

        results.append({
            "job_id": job["id"],
            "title": job["title"],
            "score": float(score),
            "distance_km": float(distance),
            "similarity": float(similarity)
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:top_n]


# -------------------------------------------------
# TEST RUN
# -------------------------------------------------

if __name__ == "__main__":

    print("\nTesting job recommendation engine...\n")

    test_worker_id = WORKERS_DF.iloc[0]["id"]

    results = recommend_jobs_for_worker(test_worker_id, top_n=5)

    print(f"\nTop jobs for worker {test_worker_id}:\n")

    for r in results:
        print(r)