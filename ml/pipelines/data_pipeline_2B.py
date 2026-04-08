import pandas as pd

# Load CSVs from pipeline 1
worker_skills_df = pd.read_csv("worker_skills_df.csv")
skill_master_df = pd.read_csv("skill_master_df.csv")

# Merge skill names
worker_skills_named = worker_skills_df.merge(
    skill_master_df,
    left_on="skill_id",
    right_on="id",
    how="left"
)

# Drop redundant id column
worker_skills_named = worker_skills_named.drop(columns=["id"])

# Clean + normalize text
worker_skills_named["skill_name"] = (
    worker_skills_named["skill_name"]
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")   # 🔥 IMPORTANT
)

# Remove duplicates
worker_skills_named = worker_skills_named.drop_duplicates(
    subset=["worker_id", "skill_name"]
)

# Combine skills into structured sentence
worker_skill_sentences = (
    worker_skills_named
    .groupby("worker_id")["skill_name"]
    .apply(lambda x: f"Worker skills: {', '.join(x)}")  # 🔥 CONTEXT ADDED
    .reset_index()
)

worker_skill_sentences.columns = ["worker_id", "skill_sentence"]

# Save CSV
worker_skill_sentences.to_csv("worker_skill_sentences.csv", index=False)

print("Worker skill sentences created.")
print("Total workers:", len(worker_skill_sentences))
print(worker_skill_sentences.sample(5))