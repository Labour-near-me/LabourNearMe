import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

worker_vectors = np.load("vectors/worker_vectors.npy")
job_vectors = np.load("vectors/job_vectors.npy")

similarity_matrix = cosine_similarity(worker_vectors, job_vectors)

top_scores = []

for i in range(similarity_matrix.shape[0]):
    top_scores.append(np.max(similarity_matrix[i]))

scores = np.array(top_scores)

print("----- MODEL VALIDATION -----")
print("Average Top Similarity:", scores.mean())
print("Max Similarity:", scores.max())
print("Min Similarity:", scores.min())
print("Std Deviation:", scores.std())