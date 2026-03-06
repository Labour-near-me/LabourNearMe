import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading skill sentences...")

worker_df = pd.read_csv("data/processed/worker_skill_sentences.csv")
job_df = pd.read_csv("data/processed/job_skill_sentences.csv")

worker_sentences = worker_df["skill_sentence"].astype(str).tolist()
job_sentences = job_df["skill_sentence"].astype(str).tolist()

print(f"Workers loaded: {len(worker_sentences)}")
print(f"Jobs loaded: {len(job_sentences)}")

print("Loading sentence transformer model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating worker embeddings...")

worker_vectors = model.encode(
    worker_sentences,
    show_progress_bar=True,
    convert_to_numpy=True
)

print("Generating job embeddings...")

job_vectors = model.encode(
    job_sentences,
    show_progress_bar=True,
    convert_to_numpy=True
)

print("Embeddings generated.")

print("Worker vector shape:", worker_vectors.shape)
print("Job vector shape:", job_vectors.shape)

print("Saving embeddings...")

np.save("ml/vectors/worker_vectors.npy", worker_vectors)
np.save("ml/vectors/job_vectors.npy", job_vectors)

print("Embeddings saved successfully.")