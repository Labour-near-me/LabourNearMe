import os
import ast
import pickle
import numpy as np
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity

from ml.engines.model_validator import predict_score

# -------------------------------------------------
# LOAD ENV
# -------------------------------------------------

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

kmeans = pickle.load(open(os.path.join(MODEL_DIR,"kmeans_model.pkl"),"rb"))

# -------------------------------------------------
# LOAD DATABASE
# -------------------------------------------------

def load_data():

    workers = pd.read_sql("SELECT * FROM workers", engine)
    jobs = pd.read_sql('SELECT * FROM "Jobs"', engine)

    workers["id"] = workers["id"].astype(str)
    jobs["id"] = jobs["id"].astype(str)

    return workers, jobs

# -------------------------------------------------
# EMBEDDING CONVERSION
# -------------------------------------------------

def convert_embeddings(df, column):

    vectors = []

    for v in df[column]:

        if isinstance(v,str):
            vectors.append(np.array(ast.literal_eval(v)))

        elif isinstance(v,list):
            vectors.append(np.array(v))

        else:
            vectors.append(np.zeros(384))

    return np.array(vectors)

# -------------------------------------------------
# DISTANCE
# -------------------------------------------------

def haversine(lat1,lon1,lat2,lon2):

    R=6371

    lat1,lon1,lat2,lon2 = map(np.radians,[lat1,lon1,lat2,lon2])

    dlat = lat2-lat1
    dlon = lon2-lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2*np.arcsin(np.sqrt(a))

    return R*c

# -------------------------------------------------
# RECOMMEND WORKERS
# -------------------------------------------------

def recommend_workers_for_job(job_id,top_n=5):

    job_row = JOBS_DF[JOBS_DF["id"]==job_id].iloc[0]

    job_vector = JOB_VEC[JOBS_DF.index[JOBS_DF["id"]==job_id][0]].reshape(1,-1)

    similarities = cosine_similarity(job_vector,WORKER_VEC)[0]

    candidates = []

    for i,worker in WORKERS_DF.iterrows():

        similarity = similarities[i]

        if similarity < 0.30:
            continue

        distance = haversine(
            worker["location_lat"],
            worker["location_lng"],
            job_row["location_lat"],
            job_row["location_lng"]
        )

        experience_bucket = 0
        if worker["experience_years"] > 5:
            experience_bucket = 2
        elif worker["experience_years"] > 2:
            experience_bucket = 1

        vector = np.array(WORKER_VEC[i], dtype=np.float64).reshape(1, -1)
        worker_cluster = int(kmeans.predict(vector)[0])
        
        features = pd.DataFrame([{
            "skill_similarity": similarity,
            "experience_bucket": experience_bucket,
            "avg_rating": worker["rating"],
            "distance_km": distance,
            "budget": job_row["budget"],
            "status": job_row["status"],
            "worker_cluster": worker_cluster
        }])

        score = predict_score(features)

        candidates.append({
            "worker_id":worker["id"],
            "score":score,
            "distance_km":distance,
            "rating":worker["rating"],
            "similarity":similarity
        })

    candidates = sorted(candidates,key=lambda x:x["score"],reverse=True)

    return candidates[:top_n]

# -------------------------------------------------
# INITIAL LOAD
# -------------------------------------------------

WORKERS_DF,JOBS_DF = load_data()

WORKER_VEC = convert_embeddings(WORKERS_DF,"worker_embedding")
JOB_VEC = convert_embeddings(JOBS_DF,"job_embedding")

# -------------------------------------------------
# TEST RUN
# -------------------------------------------------

if __name__ == "__main__":

    print("\nTesting recommendation engine...\n")

    # Example job id (replace with one from your database if needed)
    test_job_id = JOBS_DF.iloc[0]["id"]

    results = recommend_workers_for_job(test_job_id, top_n=5)

    print(f"\nTop workers for job {test_job_id}:\n")

    for r in results:
        print(r)