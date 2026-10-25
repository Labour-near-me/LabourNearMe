
import math

import ml.engines.workerForJob_RE as m
from sklearn.metrics.pairwise import cosine_similarity
from ml.engines.skill_taxonomy import normalize_skill_name


EARTH_RADIUS_KM = 6371.0


def calculate_distance_km(lat1, lon1, lat2, lon2):
    """Calculate the distance between two coordinates using Haversine."""
    lat1, lon1, lat2, lon2 = map(
        math.radians, (lat1, lon1, lat2, lon2)
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    a = max(0.0, min(1.0, a))
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def normalize_skills(skills):
    """Normalize skill names so recognized aliases can match."""
    return {
        normalize_skill_name(skill)
        for skill in (skills or set())
        if skill and normalize_skill_name(skill)
    }


def main():
    print("Refreshing recommendation data...")

    m.refresh_data(force=True)

    if m.JOBS_DF.empty or m.WORKERS_DF.empty:
        print("ERROR: Jobs or workers data is empty after refresh.")
        return

    if m.JOB_VEC.shape[0] != len(m.JOBS_DF):
        print("ERROR: Job vector count does not match job count.")
        print("Jobs:", len(m.JOBS_DF), "Job vectors:", m.JOB_VEC.shape)
        return

    if m.WORKER_VEC.shape[0] != len(m.WORKERS_DF):
        print("ERROR: Worker vector count does not match worker count.")
        print("Workers:", len(m.WORKERS_DF), "Worker vectors:", m.WORKER_VEC.shape)
        return

    similarities = cosine_similarity(m.JOB_VEC, m.WORKER_VEC)

    print(f"Jobs loaded: {len(m.JOBS_DF)}")
    print(f"Workers loaded: {len(m.WORKERS_DF)}")
    print(f"Similarity matrix: {similarities.shape}")
    print(f"Similarity threshold: {m.SIMILARITY_THRESHOLD}")
    print(f"Maximum distance: {m.MAX_DISTANCE_KM} km")
    print("\nSearching for nearby pairs with matching skills but low similarity...\n")

    found = False
    checked_pairs = 0
    skipped_coordinates = 0

    for ji, (_, job) in enumerate(m.JOBS_DF.iterrows()):
        job_id = str(job["id"])
        job_skills = normalize_skills(
            m.JOB_SKILL_MAP.get(job_id, set())
        )

        if not job_skills:
            continue

        for wi, (_, worker) in enumerate(m.WORKERS_DF.iterrows()):
            worker_id = str(worker["id"])
            worker_skills = normalize_skills(
                m.WORKER_SKILL_MAP.get(worker_id, set())
            )

            common_skills = job_skills & worker_skills

            if not common_skills:
                continue

            try:
                distance = calculate_distance_km(
                    float(job["location_lat"]),
                    float(job["location_lng"]),
                    float(worker["location_lat"]),
                    float(worker["location_lng"]),
                )
            except (TypeError, ValueError, KeyError):
                skipped_coordinates += 1
                continue

            similarity = float(similarities[ji, wi])
            checked_pairs += 1

            if (
                distance <= m.MAX_DISTANCE_KM
                and similarity < m.SIMILARITY_THRESHOLD
            ):
                print("Found a diagnostic candidate:")
                print("Job ID:", job_id)
                print("Worker ID:", worker_id)
                print("Common skills:", sorted(common_skills))
                print("Distance:", round(distance, 2), "km")
                print("Cosine similarity:", round(similarity, 4))
                print("Threshold:", m.SIMILARITY_THRESHOLD)
                found = True
                break

        if found:
            break

    if not found:
        print(
            "No nearby, matching-skill pair below the similarity threshold "
            "was found in this scan."
        )

    print("\nDiagnostic summary")
    print("Pairs checked:", checked_pairs)
    print("Pairs skipped due to missing/invalid coordinates:", skipped_coordinates)


if __name__ == "__main__":
    main()
