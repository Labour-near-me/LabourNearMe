import os
import uuid
import random
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

connection_string = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
)

engine = create_engine(connection_string)

def generate_realistic_rating():
    r = random.random()
    if r < 0.50:
        return 5
    elif r < 0.80:
        return 4
    elif r < 0.95:
        return 3
    elif r < 0.98:
        return 2
    else:
        return 1

with engine.connect() as conn:

    # 1️⃣ Completed jobs
    completed_jobs = pd.read_sql("""
        SELECT id, employer_id
        FROM "Jobs"
        WHERE status = 'completed';
    """, conn)

    # 2️⃣ Already rated jobs
    rated_jobs = pd.read_sql("""
        SELECT DISTINCT job_id FROM ratings;
    """, conn)

    # 3️⃣ Find completed jobs without rating
    unrated_jobs = completed_jobs[
        ~completed_jobs['id'].isin(rated_jobs['job_id'])
    ]

    print(f"Completed jobs: {len(completed_jobs)}")
    print(f"Already rated jobs: {len(rated_jobs)}")
    print(f"Unrated completed jobs: {len(unrated_jobs)}")

    new_ratings_inserted = 0

    for _, row in unrated_jobs.iterrows():

        job_id = row["id"]
        employer_id = row["employer_id"]

        # 4️⃣ Find accepted worker
        worker = pd.read_sql(f"""
            SELECT worker_id
            FROM applications
            WHERE job_id = '{job_id}'
            AND status = 'accepted'
            LIMIT 1;
        """, conn)

        if worker.empty:
            continue

        worker_id = worker.iloc[0]["worker_id"]

        rating_id = str(uuid.uuid4())
        rating_value = generate_realistic_rating()
        feedback = "Auto-generated feedback for dataset enhancement."
        created_at = datetime.utcnow()

        conn.execute(text("""
            INSERT INTO ratings
            (id, job_id, reviewer_id, reviewee_id, created_at, rating_value, feedback)
            VALUES
            (:id, :job_id, :reviewer_id, :reviewee_id, :created_at, :rating_value, :feedback)
        """), {
            "id": rating_id,
            "job_id": job_id,
            "reviewer_id": employer_id,
            "reviewee_id": worker_id,
            "created_at": created_at,
            "rating_value": rating_value,
            "feedback": feedback
        })

        new_ratings_inserted += 1

        if new_ratings_inserted >= 150:
            break

    print(f"✅ New ratings inserted: {new_ratings_inserted}")