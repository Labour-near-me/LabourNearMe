import pandas as pd

def precision_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)

    hits = 0
    for item in recommended_k:
        if item in relevant_set:
            hits += 1

    return hits / k


def recall_at_k(recommended, relevant, k):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)

    hits = 0
    for item in recommended_k:
        if item in relevant_set:
            hits += 1

    if len(relevant_set) == 0:
        return 0

    return hits / len(relevant_set)


def evaluate_recommendations(recommendations, ground_truth, k=5):

    precision_scores = []
    recall_scores = []

    for worker_id in recommendations:

        recommended_jobs = recommendations[worker_id]

        if worker_id not in ground_truth:
            continue

        relevant_jobs = ground_truth[worker_id]

        precision = precision_at_k(recommended_jobs, relevant_jobs, k)
        recall = recall_at_k(recommended_jobs, relevant_jobs, k)

        precision_scores.append(precision)
        recall_scores.append(recall)

    avg_precision = sum(precision_scores) / len(precision_scores)
    avg_recall = sum(recall_scores) / len(recall_scores)

    return avg_precision, avg_recall


if __name__ == "__main__":

    # Example Recommendations
    recommendations = {
        1: [10, 20, 30, 40, 50],
        2: [11, 22, 33, 44, 55],
        3: [15, 25, 35, 45, 55]
    }

    # Ground Truth (Actual jobs workers applied or clicked)
    ground_truth = {
        1: [20, 40],
        2: [22, 33],
        3: [35]
    }

    precision, recall = evaluate_recommendations(
        recommendations,
        ground_truth,
        k=5
    )

    print("Precision@5:", precision)
    print("Recall@5:", recall)