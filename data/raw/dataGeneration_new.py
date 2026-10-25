import os
import random
import uuid
from datetime import datetime
from collections import defaultdict

import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Configure it in your environment."
    )

# This script deletes and regenerates database records.
# Refuse to run unless explicitly enabled for a safe test database.
if os.getenv("ALLOW_DESTRUCTIVE_DATA_RESET") != "YES":
    raise RuntimeError(
        "Data generation is disabled by default. "
        "Use a separate test database and explicitly enable it first."
    )

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

print("Connected to database")

# -------------------------------------------------
# PARAMETERS
# -------------------------------------------------

NUM_JOBS = 2000
MAX_SKILLS_PER_JOB = 3

CITY_LAT_RANGE = (23.1500, 23.2000)
CITY_LNG_RANGE = (75.7500, 75.8500)

ALLOWED_JOB_STATUS = ['open','assigned','completed','cancelled']
JOB_STATUS_WEIGHTS = [0.5,0.2,0.2,0.1]

# -------------------------------------------------
# CLEAN OLD DATA
# -------------------------------------------------

print("Clearing old job related tables...")

cursor.execute('DELETE FROM applications')
cursor.execute('DELETE FROM ratings')
cursor.execute('DELETE FROM "Job_required_skill"')
cursor.execute('DELETE FROM "Jobs"')

conn.commit()

print("Old data cleared")

# -------------------------------------------------
# LOAD SKILLS
# -------------------------------------------------

cursor.execute('SELECT id, skill_name, category FROM "Skill_master"')
skills = cursor.fetchall()

category_to_skills = defaultdict(list)

for skill_id, skill_name, category in skills:
    category_to_skills[category].append((skill_id, skill_name))

categories = list(category_to_skills.keys())

print(f"Loaded {len(categories)} categories")

# -------------------------------------------------
# LOAD EMPLOYERS
# -------------------------------------------------

cursor.execute('SELECT id FROM "Employers"')
employers = [row[0] for row in cursor.fetchall()]

print(f"Loaded {len(employers)} employers")

# -------------------------------------------------
# LOAD WORKERS
# -------------------------------------------------

cursor.execute('SELECT id, rating FROM workers')
workers_db = cursor.fetchall()

workers = []

for worker_id, rating in workers_db:

    cursor.execute(
        'SELECT skill_id FROM "Worker_skills" WHERE worker_id=%s',
        (worker_id,)
    )

    worker_skills = [row[0] for row in cursor.fetchall()]

    workers.append({
        "id": worker_id,
        "skills": worker_skills,
        "rating": rating
    })

print(f"Loaded {len(workers)} workers")

# -------------------------------------------------
# JOB DESCRIPTION TEMPLATES
# -------------------------------------------------

job_templates = [
    "We are looking for an experienced {skill} professional.",
    "Hiring skilled worker for {category} related tasks.",
    "Need expert in {skill} for {category} work."
]

feedback_templates = [
    "Excellent work on {skill}.",
    "Worker completed {skill} task professionally.",
    "Very satisfied with {skill} work."
]

# -------------------------------------------------
# GENERATE JOBS
# -------------------------------------------------

jobs = []

print("Generating jobs...")

for i in range(NUM_JOBS):

    job_id = str(uuid.uuid4())

    employer_id = random.choice(employers)

    category = random.choice(categories)

    category_skills = category_to_skills[category]

    required_skills = random.sample(
        category_skills,
        random.randint(1, min(MAX_SKILLS_PER_JOB, len(category_skills)))
    )

    main_skill_name = required_skills[0][1]

    title = f"{category} Job - {main_skill_name}"

    description = random.choice(job_templates).format(
        skill=main_skill_name,
        category=category.lower()
    )

    budget = 500 + len(required_skills)*200 + random.randint(-50,50)

    status = random.choices(
        ALLOWED_JOB_STATUS,
        weights=JOB_STATUS_WEIGHTS,
        k=1
    )[0]

    lat = random.uniform(*CITY_LAT_RANGE)
    lng = random.uniform(*CITY_LNG_RANGE)

    cursor.execute("""
        INSERT INTO "Jobs"
        (id, employer_id, title, description, budget, status,
         created_at, location_lat, location_lng)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,(
        job_id,
        employer_id,
        title,
        description,
        budget,
        status,
        datetime.now(),
        lat,
        lng
    ))

    for skill_id, skill_name in required_skills:

        cursor.execute("""
            INSERT INTO "Job_required_skill"
            (job_id, skill_id)
            VALUES (%s,%s)
        """,(job_id,skill_id))

    jobs.append({
        "id": job_id,
        "skills": [s[0] for s in required_skills],
        "status": status,
        "employer": employer_id,
        "skill": main_skill_name
    })

conn.commit()

print(f"{len(jobs)} jobs generated")

# -------------------------------------------------
# GENERATE APPLICATIONS + RATINGS
# -------------------------------------------------

application_count = 0
rating_count = 0

print("Generating applications and ratings...")

for job in jobs:

    for worker in random.sample(workers, 10):

        try:

            if set(worker["skills"]) & set(job["skills"]):

                status = random.choices(
                    ['pending','accepted','shortlisted','rejected'],
                    weights=[0.4,0.3,0.2,0.1],
                    k=1
                )[0]

                cursor.execute("""
                    INSERT INTO applications
                    (id, job_id, worker_id, status, applied_at)
                    VALUES (%s,%s,%s,%s,%s)
                """,(
                    str(uuid.uuid4()),
                    job["id"],
                    worker["id"],
                    status,
                    datetime.now()
                ))

                application_count += 1

                if job["status"] == "completed" and status in ["accepted","shortlisted"]:

                    rating_value = round(
                        min(5,max(1,worker["rating"]+random.uniform(-1,1)))
                    )

                    feedback = random.choice(feedback_templates).format(
                        skill=job["skill"]
                    )

                    cursor.execute("""
    INSERT INTO ratings
    (id, job_id, reviewer_id, reviewee_id,
     rating_value, feedbck, created_at)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
""",(
                        str(uuid.uuid4()),
                        job["id"],
                        job["employer"],
                        worker["id"],
                        rating_value,
                        feedback,
                        datetime.now()
                    ))

                    rating_count += 1

        except Exception as e:
            print("Error:",e)
            conn.rollback()

conn.commit()

print(f"{application_count} applications created")
print(f"{rating_count} ratings created")

# -------------------------------------------------
# UPDATE EMPLOYER RATINGS
# -------------------------------------------------

cursor.execute('SELECT id FROM "Employers"')
employers = [row[0] for row in cursor.fetchall()]

for emp in employers:

    cursor.execute("""
        SELECT AVG(rating_value)
        FROM ratings r
        JOIN "Jobs" j ON j.id = r.job_id
        WHERE j.employer_id=%s
    """,(emp,))

    avg_rating = cursor.fetchone()[0]

    if avg_rating:

        cursor.execute("""
            UPDATE "Employers"
            SET rating=%s
            WHERE id=%s
        """,(round(avg_rating,2),emp))

conn.commit()

cursor.close()
conn.close()

print("Employer ratings updated")
print("Job data generation completed successfully 🚀")