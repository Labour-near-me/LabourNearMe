
"""Explicit skill compatibility rules shared by both recommendation engines.

Eligibility must not be decided by embedding similarity alone: unrelated trades
can have high semantic similarity. Add new cross-skill relationships explicitly
in _SKILL_ALIASES / _COMPATIBLE_SKILLS after domain review.
"""

import re


def normalize_skill_name(value: str) -> str:
    """Normalize case, whitespace, and common punctuation for comparisons."""
    text = str(value or "").casefold().strip()
    text = re.sub(r"[_/\\-]+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


# Genuine labels and spelling variants only.
# Unrelated occupations must never be aliases.
_SKILL_ALIASES = {
    "plumbing": "plumber",
    "plumbing work": "plumber",
    "plumber work": "plumber",
    "electrician work": "electrician",
    "electrical work": "electrician",
    "electrical wiring": "electrical wiring",
    "wiring installation": "electrical wiring",
    "switchboard repair": "switch repair",
    "switch repair": "switch repair",
}

# Explicit, narrow compatibility relationships.
_COMPATIBLE_SKILLS = {
    "electrician": {"electrical wiring", "switch repair"},
}


def canonical_skill_name(value: str) -> str:
    normalized = normalize_skill_name(value)
    return _SKILL_ALIASES.get(normalized, normalized)


def skills_match(worker_skill: str, required_skill: str) -> bool:
    """Match exact normalized/aliased skills or explicit compatible skills."""
    worker = canonical_skill_name(worker_skill)
    required = canonical_skill_name(required_skill)

    if not worker or not required:
        return False

    if worker == required:
        return True

    if required in _COMPATIBLE_SKILLS.get(worker, set()):
        return True

    if worker in _COMPATIBLE_SKILLS.get(required, set()):
        return True

    return False


def skill_match_score(worker_skill: str, required_skill: str) -> float:
    """Binary eligibility score; semantic similarity is not a hard skill match."""
    return 1.0 if skills_match(worker_skill, required_skill) else 0.0


def matched_required_skills(worker_skills, required_skills) -> set[str]:
    """Return distinct required skills covered by at least one worker skill."""
    worker_names = [
        canonical_skill_name(skill)
        for skill in worker_skills
    ]

    matched = set()

    for required_skill in required_skills:
        canonical_required = canonical_skill_name(required_skill)

        if canonical_required and any(
            skills_match(worker_name, canonical_required)
            for worker_name in worker_names
        ):
            matched.add(canonical_required)

    return matched


def prepare_skill_embeddings(skill_names) -> None:
    """Compatibility no-op retained for existing engine refresh calls."""
    return None
