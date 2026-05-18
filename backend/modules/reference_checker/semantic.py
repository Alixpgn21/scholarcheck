"""
Vérification d'inférence logique (NLI) entre la phrase citante et l'abstract du papier cité.
Utilise un modèle Cross-Encoder pour détecter l'Entailment (implication) ou la Contradiction.
"""
from sentence_transformers import CrossEncoder
import numpy as np

_model = None

def _get_model():
    global _model
    if _model is None:
        from config import NLI_MODEL
        _model = CrossEncoder(NLI_MODEL)
    return _model

def compute_similarity(citing_sentence: str, abstract: str) -> dict:
    """
    Retourne un score d'inférence logique entre l'abstract (prémisse) et la phrase (hypothèse).
    Label 0: contradiction, Label 1: entailment, Label 2: neutral.
    """
    if not citing_sentence or not abstract:
        return {"score": None, "label": "indéterminé", "reason": "Données manquantes."}

    model = _get_model()
    # Le modèle prend des paires [Prémisse, Hypothèse]
    scores = model.predict([(abstract, citing_sentence)])[0]
    
    # Softmax pour obtenir des probabilités
    exp_scores = np.exp(scores - np.max(scores))
    probs = exp_scores / exp_scores.sum()
    
    # Pour cross-encoder/nli-distilroberta-base :
    # 0 = contradiction, 1 = entailment, 2 = neutral
    contradiction_prob = probs[0]
    entailment_prob = probs[1]
    neutral_prob = probs[2]
    
    if entailment_prob > 0.45:
        label = "pertinent"
        reason = "L'abstract soutient logiquement la phrase citante (Entailment)."
        score = entailment_prob
    elif contradiction_prob > 0.45:
        label = "suspect"
        reason = "L'abstract contredit la phrase citante (Contradiction)."
        score = contradiction_prob
    else:
        label = "ambigu"
        reason = "L'abstract ne confirme ni n'infirme clairement la phrase citante (Neutral)."
        score = neutral_prob

    return {"score": round(float(score), 3), "label": label, "reason": reason}
