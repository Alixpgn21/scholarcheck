"""
Vérifie l'existence et la cohérence d'une référence bibliographique.
"""
import asyncio
from .api_client import query_crossref, query_openalex, query_semantic_scholar


YEAR_TOLERANCE = 1  # Tolérance ±1 an sur l'année


async def verify_reference(raw_ref: str, expected_year: int = None, expected_authors: list[str] = None) -> dict:
    """
    Interroge les 3 APIs en parallèle et consolide le résultat.
    Retourne un rapport de vérification.
    """
    crossref, openalex, semantic = await asyncio.gather(
        query_crossref(title=raw_ref),
        query_openalex(title=raw_ref),
        query_semantic_scholar(title=raw_ref),
    )

    results = [r for r in [crossref, openalex, semantic] if r]

    if not results:
        return {
            "status": "not_found",
            "confidence": 0.0,
            "message": "Aucune source n'a trouvé cette référence.",
            "sources": [],
            "best_match": None,
        }

    best = _pick_best(results)
    issues = _check_consistency(best, expected_year, expected_authors)

    confidence = _compute_confidence(results, issues)

    return {
        "status": "warning" if issues else "ok",
        "confidence": confidence,
        "message": "; ".join(issues) if issues else "Référence vérifiée.",
        "sources": [r["source"] for r in results],
        "best_match": best,
    }


def _pick_best(results: list[dict]) -> dict:
    # Priorité CrossRef > OpenAlex > Semantic Scholar
    priority = {"crossref": 0, "openalex": 1, "semantic_scholar": 2}
    return sorted(results, key=lambda r: priority.get(r["source"], 99))[0]


def _check_consistency(match: dict, expected_year: int | None, expected_authors: list[str] | None) -> list[str]:
    issues = []

    if expected_year and match.get("year"):
        if abs(match["year"] - expected_year) > YEAR_TOLERANCE:
            issues.append(f"Année incorrecte : trouvé {match['year']}, attendu {expected_year}")

    if expected_authors and match.get("authors"):
        found_families = {a.split()[-1].lower() for a in match["authors"] if a}
        expected_families = {a.split()[-1].lower() for a in expected_authors if a}
        missing = expected_families - found_families
        if missing:
            issues.append(f"Auteurs non trouvés : {', '.join(missing)}")

    return issues


def _compute_confidence(results: list[dict], issues: list[str]) -> float:
    base = min(len(results) / 3, 1.0)  # 0.33 / 0.66 / 1.0 selon nb de sources
    penalty = len(issues) * 0.2
    return round(max(0.0, base - penalty), 2)
