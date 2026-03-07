import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

worker_vec = np.load("vectors/worker_vectors.npy")
job_vec = np.load("vectors/job_vectors.npy")

sim = cosine_similarity(worker_vec[0].reshape(1,-1), job_vec)

print("Top similarities:")
print(np.sort(sim[0])[-10:])