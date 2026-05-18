"""
Comparaison sémantique entre la phrase citante et l'abstract du papier cité.
"""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

_model = None


def _get_model():
    global _model
    if _model is None:
        from config import EMBEDDING_MODEL
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def compute_similarity(citing_sentence: str, abstract: str) -> dict:
    """
    Retourne un score de similarité cosinus entre la phrase citante et l'abstract.
    Score > 0.5 → pertinent, 0.3–0.5 → ambigu, < 0.3 → suspect.
    """
    if not citing_sentence or not abstract:
        return {"score": None, "label": "indéterminé", "reason": "Données manquantes."}

    model = _get_model()
    embeddings = model.encode([citing_sentence, abstract])
    score = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])

    label, reason = _interpret(score)
    return {"score": round(score, 3), "label": label, "reason": reason}


def _interpret(score: float) -> tuple[str, str]:
    if score >= 0.5:
        return "pertinent", "La phrase citante est bien soutenue par l'abstract."
    elif score >= 0.3:
        return "ambigu", "Lien sémantique faible — vérification manuelle recommandée."
    else:
        return "suspect", "La phrase citante ne semble pas soutenue par ce papier."
