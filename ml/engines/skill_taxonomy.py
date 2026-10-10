"""Small, explicit skill taxonomy used by both recommendation directions."""

from functools import lru_cache

import numpy as np

from backend.services.embedding_service import encode_text


# Skill-name embeddings are compared separately from whole-profile embeddings.
# A conservative cutoff reduces false matches between broad occupational text.
SEMANTIC_SKILL_THRESHOLD = 0.70


def normalize_skill_name(value: str) -> str:
    return " ".join(str(value).strip().casefold().split())


# Canonicalize spelling/label variants that mean the same specific skill.
_SKILL_ALIASES = {
    "electrical wiring": "electrical wiring",
    "wiring installation": "electrical wiring",
    "switch repair": "switch repair",
    "switchboard repair": "switch repair",
}

# A broad electrician skill can satisfy a specific electrician requirement,
# and a specific electrician skill can satisfy a broad electrician job.
# The specific skills are deliberately not interchangeable with each other.
_ELECTRICIAN_SKILLS = {
    "electrical wiring",
    "switch repair",
}


def canonical_skill_name(value: str) -> str:
    normalized = normalize_skill_name(value)
    return _SKILL_ALIASES.get(normalized, normalized)


def skills_match(worker_skill: str, required_skill: str) -> bool:
    worker = canonical_skill_name(worker_skill)
    required = canonical_skill_name(required_skill)

    if worker == required:
        return True

    if worker == "electrician" and required in _ELECTRICIAN_SKILLS:
        return True

    if required == "electrician" and worker in _ELECTRICIAN_SKILLS:
        return True

    return False


@lru_cache(maxsize=512)
def _skill_embedding(skill_name: str) -> np.ndarray:
    """Embed a normalized skill once per process and reuse it across matches."""
    # Add a short context so terse catalog labels are compared as skills.
    return np.asarray(encode_text(f"Trade skill: {skill_name}"), dtype=float)


def semantic_skill_similarity(first_skill: str, second_skill: str) -> float:
    """Return cosine similarity between two skill labels, or zero if invalid."""
    first = normalize_skill_name(first_skill)
    second = normalize_skill_name(second_skill)
    if not first or not second:
        return 0.0

    first_vector = _skill_embedding(first)
    second_vector = _skill_embedding(second)
    denominator = np.linalg.norm(first_vector) * np.linalg.norm(second_vector)
    if denominator == 0:
        return 0.0
    return float(np.dot(first_vector, second_vector) / denominator)


def skill_match_score(worker_skill: str, required_skill: str) -> float:
    """Score a skill pair: exact/taxonomy matches win, else use semantic text."""
    if skills_match(worker_skill, required_skill):
        return 1.0
    return semantic_skill_similarity(worker_skill, required_skill)


def matched_required_skills(worker_skills, required_skills) -> set[str]:
    """Return the distinct job requirements covered by a worker's skills."""
    return {
        required_skill
        for required_skill in required_skills
        if any(
            skill_match_score(worker_skill, required_skill) >= SEMANTIC_SKILL_THRESHOLD
            for worker_skill in worker_skills
        )
    }
