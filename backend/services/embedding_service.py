"""Shared, lazy-loaded sentence embedding model for API services."""

from functools import lru_cache
from threading import Lock

from sentence_transformers import SentenceTransformer


_model_lock = Lock()


@lru_cache(maxsize=1)
def _load_model() -> SentenceTransformer:
    # Serialize initial loading so simultaneous first requests cannot each
    # allocate a separate copy of the transformer model.
    with _model_lock:
        return SentenceTransformer("all-MiniLM-L6-v2")


def encode_texts(texts: list[str]) -> list[list[float]]:
    """Encode a batch with the shared model to avoid repeated model calls."""
    if not texts:
        return []
    vectors = _load_model().encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        convert_to_numpy=True,
    )
    return vectors.tolist()


def encode_text(text: str) -> list[float]:
    return encode_texts([text])[0]
