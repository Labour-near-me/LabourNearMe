import psycopg2
from faker import Faker
import random
import uuid
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
NUM_WORKERS = 400
NUM_EMPLOYERS = 80
NUM_JOBS = 250

fake = Faker()

conn = psycopg2.connect(
    host="aws-1-ap-south-1.pooler.supabase.com",
    database="postgres",
    user="postgres.ihnlpiujpjslpgesqimj",
    password="subArAshii325",
    port="6543"
)

cursor = conn.cursor()

# -----------------------------
# FETCH SKILLS
# -----------------------------
cursor.execute('SELECT id FROM "Skill_master";')
all_skills = [row[0] for row in cursor.fetchall()]

# -----------------------------
# CREATE EMPLOYERS
# -----------------------------
employer_ids = []

for _ in range(NUM_EMPLOYERS):
    pid = str(uuid.uuid4())
    employer_ids.append(pid)

    cursor.execute("""
        INSERT INTO "Profiles" (id, full_name, phone, role)
        VALUES (%s, %s, %s, %s)
    """, (pid, fake.name(), fake.msisdn()[:10], 'employer'))

conn.commit()

# -----------------------------
# CREATE WORKERS
# -----------------------------
worker_ids = []

for _ in range(NUM_WORKERS):
    pid = str(uuid.uuid4())
    worker_ids.append(pid)

    cursor.execute("""
        INSERT INTO "Profiles"(id, full_name, phone, role)
        VALUES (%s, %s, %s, %s)
    """, (pid, fake.name(), fake.msisdn()[:10], 'worker'))

    experience = int(np.random.choice(
        [random.randint(0,2), random.randint(3,6), random.randint(7,12)],
        p=[0.4,0.35,0.25]
    ))

    base_wage = random.randint(400,800)
    expected_wage = int(base_wage + experience * 40 + random.randint(-50,50))
    rating = round(min(5.0, 3.5 + experience*0.05 + random.uniform(-0.3,0.3)),1)

    lat = 28.4 + random.uniform(-0.1,0.1)
    lng = 77.0 + random.uniform(-0.1,0.1)

    cursor.execute("""
        INSERT INTO workers 
        (id, experience_years, expected_wage, location_lat, location_lng,
         availability_status, rating, total_jobs_done)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (pid, experience, expected_wage, lat, lng, True, rating, 0))

conn.commit()

# -----------------------------
# ASSIGN WORKER SKILLS
# -----------------------------
for wid in worker_ids:
    skills = random.sample(all_skills, random.randint(2,5))

    for sid in skills:
        cursor.execute("""
            INSERT INTO "Worker_skills" (worker_id, skill_id)
            VALUES (%s,%s)
            ON CONFLICT DO NOTHING
        """, (wid, sid))

conn.commit()

# -----------------------------
# CREATE JOBS (RLS-safe & Check-safe)
# -----------------------------
job_ids = []

for _ in range(NUM_JOBS):
    jid = str(uuid.uuid4())
    job_ids.append(jid)

    # Pick a random employer
    employer = random.choice(employer_ids)

    # Job details
    title = fake.sentence(nb_words=4)
    description = fake.paragraph()
    budget = random.randint(500, 3000)
    lat = 28.4 + random.uniform(-0.1, 0.1)
    lng = 77.0 + random.uniform(-0.1, 0.1)

    # Status: ensure it matches check constraint exactly
    status = random.choice(['open', 'in_progress', 'completed']).strip()

    # Insert into Jobs table
    cursor.execute("""
        INSERT INTO "Jobs"
        (id, employer_id, title, description, budget,
         status, created_at, location_lat, location_lng)
        VALUES (%s,%s,%s,%s,%s,%s,now(),%s,%s)
    """, (
        jid,
        employer,
        title,
        description,
        budget,
        status,
        lat,
        lng
    ))

    # Assign required skills to the job
    required_skills = random.sample(all_skills, random.randint(1, 3))
    for sid in required_skills:
        cursor.execute("""
            INSERT INTO "Job_required_skills" (job_id, skill_id)
            VALUES (%s,%s)
            ON CONFLICT DO NOTHING
        """, (jid, sid))

conn.commit()

# -----------------------------
# GENERATE APPLICATIONS (SMART LOGIC)
# -----------------------------
for jid in job_ids:

    cursor.execute("""
        SELECT skill_id FROM "Job_required_skills"
        WHERE job_id = %s
    """, (jid,))
    job_skills = set([row[0] for row in cursor.fetchall()])

    for wid in random.sample(worker_ids, 30):  # 30 candidates per job

        cursor.execute("""
            SELECT skill_id FROM "Worker_skills"
            WHERE worker_id = %s
        """, (wid,))
        worker_skills = set([row[0] for row in cursor.fetchall()])

        overlap = len(job_skills & worker_skills)

        if overlap == 0:
            continue

        if overlap >= 2:
            status = str(np.random.choice(
                ['accepted','shortlisted','rejected'],
                p=[0.3,0.4,0.3]
            ))
        else:
            status =str(np.random.choice(
                ['shortlisted','rejected'],
                p=[0.2,0.8]
            ))

        cursor.execute("""
            INSERT INTO "Applications"
            (id, job_id, worker_id, status, applied_at)
            VALUES (%s,%s,%s,%s,now())
            ON CONFLICT DO NOTHING
        """, (str(uuid.uuid4()), jid, wid, status))

conn.commit()

cursor.close()
conn.close()

print("Data generation completed successfully 🚀")