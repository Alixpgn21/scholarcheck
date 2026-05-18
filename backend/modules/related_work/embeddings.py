"""
Génération d'embeddings pour un corpus de documents scientifiques.
"""
from sentence_transformers import SentenceTransformer
import numpy as np

_model = None


def _get_model():
    global _model
    if _model is None:
        from config import EMBEDDING_MODEL
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_documents(documents: list[dict]) -> np.ndarray:
    """
    documents : liste de {"id": str, "title": str, "abstract": str, ...}
    Retourne une matrice (N, D) d'embeddings.
    """
    model = _get_model()
    texts = [_doc_to_text(d) for d in documents]
    return model.encode(texts, show_progress_bar=False)


def _doc_to_text(doc: dict) -> str:
    title = doc.get("title") or ""
    abstract = doc.get("abstract") or ""
    return f"{title}. {abstract}".strip()
