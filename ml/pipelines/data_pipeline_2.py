import pandas as pd

# Load CSVs
job_skills_df = pd.read_csv("job_skills_df.csv")
skill_master_df = pd.read_csv("skill_master_df.csv")

# Merge correctly
job_skills_named = job_skills_df.merge(
    skill_master_df,
    left_on="skill_id",
    right_on="id",
    how="left"
)

# Drop redundant id column
job_skills_named = job_skills_named.drop(columns=["id"])

# Clean skill text
job_skills_named["skill_name"] = (
    job_skills_named["skill_name"]
    .str.lower()
    .str.strip()
)

# Remove duplicate skill entries per job
job_skills_named = job_skills_named.drop_duplicates(
    subset=["job_id", "skill_name"]
)

# Group and combine into single sentence per job
job_skill_sentences = (
    job_skills_named
    .groupby("job_id")["skill_name"]
    .apply(lambda x: " ".join(x))
    .reset_index()
)

job_skill_sentences.columns = ["job_id", "skill_sentence"]

# Save to CSV
job_skill_sentences.to_csv("job_skill_sentences.csv", index=False)

print("Job skill sentences created.")
print("Total jobs:", len(job_skill_sentences))
print(job_skill_sentences.sample(5))