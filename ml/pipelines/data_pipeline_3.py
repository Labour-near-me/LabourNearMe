import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text
import numpy as np
import re
import os

# -----------------------
# 1️⃣ Load worker and job skill sentences
# -----------------------
# Using absolute paths is safer
BASE_DIR = os.getcwd()
WORKER_CSV = os.path.join(BASE_DIR, "data", "processed", "worker_skill_sentences.csv")
JOB_CSV = os.path.join(BASE_DIR, "data", "processed", "job_skill_sentences.csv")

worker_df = pd.read_csv(WORKER_CSV)
job_df = pd.read_csv(JOB_CSV)

print(f"Workers loaded: {len(worker_df)}")
print(f"Jobs loaded: {len(job_df)}")


# -----------------------
# 2️⃣ Improved Text Cleaning
# -----------------------
def clean_text(text_data):
    text_data = str(text_data).lower()
    # Remove special characters and numbers
    text_data = re.sub(r'[^a-zA-Z ]', ' ', text_data)
    # Remove extra whitespace
    text_data = re.sub(r'\s+', ' ', text_data)
    return text_data.strip()

worker_df["skill_sentence"] = worker_df["skill_sentence"].apply(clean_text)
job_df["skill_sentence"] = job_df["skill_sentence"].apply(clean_text)


# -----------------------
# 3️⃣ TF-IDF with Noise Filtering
# -----------------------
# Add domain-specific noise words to standard English stop words
custom_noise = ["job", "service", "management", "worker", "tasks", "general", "expert", "skills"]
stop_words = list(text.ENGLISH_STOP_WORDS.union(custom_noise))

vectorizer = TfidfVectorizer(
    stop_words=stop_words,
    ngram_range=(1, 2),  # Captures "oil change" as one feature
    min_df=1,            # Allow rare specialized skills
    max_df=0.7,          # Ignore terms that appear in more than 70% of docs
    max_features=425     # Keeping your 425 dimensions as requested
)

# Fit on both to ensure the vocabulary covers all possible skills
all_sentences = pd.concat([worker_df["skill_sentence"], job_df["skill_sentence"]])
vectorizer.fit(all_sentences)

worker_vectors = vectorizer.transform(worker_df["skill_sentence"])
job_vectors = vectorizer.transform(job_df["skill_sentence"])

print(f"TF-IDF complete. Vector Shape: {worker_vectors.shape}")

# -----------------------
# 4️⃣ Save vectors
# -----------------------
os.makedirs("ml/vectors", exist_ok=True)
np.save("ml/vectors/worker_vectors.npy", worker_vectors.toarray())
np.save("ml/vectors/job_vectors.npy", job_vectors.toarray())

print("Vector files saved to ml/vectors/")


# -----------------------
# 5️⃣ Validation: Print Top Features
# -----------------------
# This helps you see if the 425 features are actually useful skills
feature_names = vectorizer.get_feature_names_out()
print("\n🔍 Sample of extracted Skill Features:")
print(feature_names[:20]) 


# -----------------------
# 6️⃣ Cosine Similarity & Similarity Dataset
# -----------------------
similarity_matrix = cosine_similarity(worker_vectors, job_vectors)
records = []

for w_idx, worker_id in enumerate(worker_df["worker_id"]):
    # Top 10 matches
    top_jobs = np.argsort(similarity_matrix[w_idx])[-10:]
    for j_idx in top_jobs:
        records.append({
            "worker_id": worker_id,
            "job_id": job_df.iloc[j_idx]["job_id"],
            "skill_similarity": float(similarity_matrix[w_idx][j_idx])
        })

similarity_df = pd.DataFrame(records)
similarity_df.to_csv("data/processed/worker_job_similarity.csv", index=False)

print("\n✅ Pipeline completed successfully.")