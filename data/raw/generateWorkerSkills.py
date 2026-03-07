import psycopg2
import random
from collections import defaultdict

# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------

conn = psycopg2.connect(
    host="aws-1-ap-south-1.pooler.supabase.com",
    database="postgres",
    user="postgres.ihnlpiujpjslpgesqimj",
    password="subArAshii325",
    port="6543"
)

cursor = conn.cursor()

print("Connected to database")

# -------------------------------------------------
# STEP 1: FETCH SKILLS WITH CATEGORY
# -------------------------------------------------

cursor.execute('SELECT id, skill_name, category FROM "Skill_master"')
skills = cursor.fetchall()

print(f"Loaded {len(skills)} skills from Skill_master")

# -------------------------------------------------
# STEP 2: BUILD CATEGORY → SKILLS MAP
# -------------------------------------------------

category_to_skills = defaultdict(list)

for skill_id, skill_name, category in skills:
    category_to_skills[category].append((skill_id, skill_name))

categories = list(category_to_skills.keys())

print(f"Detected {len(categories)} skill categories")

# -------------------------------------------------
# STEP 3: FETCH WORKERS
# -------------------------------------------------

cursor.execute('SELECT id FROM workers')
workers = [row[0] for row in cursor.fetchall()]

print(f"Loaded {len(workers)} workers")

# -------------------------------------------------
# STEP 4: CLEAR OLD WORKER SKILLS
# -------------------------------------------------

cursor.execute('DELETE FROM "Worker_skills"')
conn.commit()

print("Old Worker_skills table cleared")

# -------------------------------------------------
# STEP 5: GENERATE NEW SKILLS FOR EACH WORKER
# -------------------------------------------------

insert_count = 0

for worker_id in workers:

    # Pick a random category
    category = random.choice(categories)

    # Skills belonging to that category
    category_skills = category_to_skills[category]

    # Choose 3–5 skills
    num_skills = random.randint(3,5)

    selected_skills = random.sample(
        category_skills,
        min(num_skills, len(category_skills))
    )

    for skill_id, skill_name in selected_skills:

        cursor.execute("""
            INSERT INTO "Worker_skills" (worker_id, skill_id)
            VALUES (%s,%s)
        """, (worker_id, skill_id))

        insert_count += 1

conn.commit()

print(f"Inserted {insert_count} worker skill records")

# -------------------------------------------------
# STEP 6: VALIDATION CHECK
# -------------------------------------------------

cursor.execute("""
SELECT worker_id, COUNT(skill_id)
FROM "Worker_skills"
GROUP BY worker_id
ORDER BY COUNT(skill_id) DESC
LIMIT 10
""")

rows = cursor.fetchall()

print("\nTop workers by skill count:")

for r in rows:
    print(r)

# -------------------------------------------------
# CLOSE CONNECTION
# -------------------------------------------------

cursor.close()
conn.close()

print("\nWorker skills regeneration completed successfully 🚀")