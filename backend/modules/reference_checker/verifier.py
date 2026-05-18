"""
Vérifie l'existence et la cohérence d'une référence bibliographique.
"""
import asyncio
from .api_client import query_crossref, query_openalex, query_semantic_scholar
import re

YEAR_TOLERANCE = 1  # Tolérance ±1 an sur l'année


def _extract_metadata_from_raw(raw_ref: str) -> tuple[int | None, list[str]]:
    """Extrait l'année et les noms d'auteurs depuis un texte de référence brut."""
    year_match = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", raw_ref)
    year = int(year_match.group(1)) if year_match else None
    # Noms avant la première parenthèse ou avant l'année : "Smith, J., & Doe, J. (2024)"
    authors_part = re.split(r"\(\d{4}\)|\.\s+[A-Z]", raw_ref)[0]
    # Extraire les noms de famille (support tirets, camelCase, accents)
    # Capture tout mot commençant par majuscule jusqu'à virgule/&/et al
    surnames = re.findall(r"\b([A-Z][A-Za-zé\-]+)(?:,|\s+&|\s+et\s+al)", authors_part)
    return year, surnames


async def verify_reference(raw_ref: str, expected_year: int = None, expected_authors: list[str] = None) -> dict:
    """
    Interroge les 3 APIs en parallèle et consolide le résultat.
    Si un DOI est trouvé dans le texte brut, on l'utilise en priorité.
    """
    doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9a-z]+", raw_ref)
    doi = doi_match.group(0) if doi_match else None

    # Auto-extraire année et auteurs si non fournis
    if expected_year is None and expected_authors is None:
        expected_year, expected_authors = _extract_metadata_from_raw(raw_ref)

    if doi:
        crossref, openalex, semantic = await asyncio.gather(
            query_crossref(doi=doi),
            query_openalex(doi=doi),
            query_semantic_scholar(doi=doi),
        )
    else:
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
    ranked = sorted(results, key=lambda r: priority.get(r["source"], 99))
    best = ranked[0]
    # CrossRef retourne rarement un abstract — on le complète depuis une autre source
    if not best.get("abstract"):
        for r in ranked[1:]:
            if r.get("abstract"):
                best = {**best, "abstract": r["abstract"]}
                break
    return best


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
