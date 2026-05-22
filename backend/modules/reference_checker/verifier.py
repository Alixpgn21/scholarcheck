"""
Vérifie l'existence et la cohérence d'une référence bibliographique.
"""
import asyncio
import re
import datetime
from .api_client import query_crossref, query_openalex, query_semantic_scholar

YEAR_TOLERANCE = 1  # Tolérance ±1 an sur l'année


def _extract_metadata_from_raw(raw_ref: str) -> tuple[int | None, list[str]]:
    """Extrait l'année et les noms d'auteurs depuis un texte de référence brut."""
    # Masquer les IDs arXiv (ex: arXiv.1810.04805) avant d'extraire l'année
    # pour éviter que "1810" soit interprété comme l'an 1810
    ref_no_arxiv = re.sub(r"[Aa]r[Xx]iv[:/.][\d.]+", "ARXIV", raw_ref)
    year_match = re.search(r"\b(1[5-9]\d{2}|20\d{2})\b", ref_no_arxiv)
    year = int(year_match.group(1)) if year_match else None

    # Si pas d'année trouvée dans le texte mais qu'un ID arXiv est présent,
    # dériver l'année depuis l'ID (ex: 1706.03762 → 2017, 1810.04805 → 2018)
    if year is None:
        arxiv_id_match = re.search(r"arXiv[:/.](\d{2})(\d{2})\.\d+", raw_ref, re.IGNORECASE)
        if arxiv_id_match:
            yy = int(arxiv_id_match.group(1))
            year = 2000 + yy if yy < 50 else 1900 + yy

    # Couper AVANT le titre : le titre commence après les auteurs
    # En LaTeX: auteurs se terminent avant ``Title'' ou "Title"
    # En texte plat: auteurs se terminent avant une majuscule suivant un point
    # On coupe aussi sur "DOI:", "URL:", "arXiv" pour éviter de capturer des métadonnées
    authors_part = re.split(
        r'``|"[A-Z]|\bDOI\b|\bURL\b|\barXiv\b|\bIn\s+[A-Z]|\bProceedings\b',
        raw_ref
    )[0]

    # Extraire les noms de famille (support tirets, camelCase, accents)
    # On exclut les abréviations venues typiques (IEEE, CVPR, ICCV, NeurIPS, etc.)
    VENUE_WORDS = {
        "IEEE", "ACM", "CVPR", "ICCV", "ECCV", "NeurIPS", "NIPS", "ICLR",
        "ICML", "EMNLP", "NAACL", "ACL", "AAAI", "IJCAI", "SIGIR", "KDD",
        "WSDM", "WWW", "VLDB", "SIGMOD", "Blog", "OpenAI", "Google", "Meta",
        "Journal", "Review", "Science", "Nature", "Letters", "Annual",
        "Conference", "Workshop", "Symposium", "Transactions",
    }
    raw_surnames = re.findall(r"\b([A-Z][A-Za-zé\-]+)(?:,|\s+&|\s+et\s+al)", authors_part)
    surnames = [s for s in raw_surnames if s not in VENUE_WORDS]
    return year, surnames


async def verify_reference(raw_ref: str, expected_year: int = None, expected_authors: list[str] = None) -> dict:
    """
    Interroge les 3 APIs en parallèle et consolide le résultat.
    Si un DOI est trouvé dans le texte brut, on l'utilise en priorité.
    Si le DOI ne retourne rien, fallback automatique par titre.
    """
    doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9a-z]+", raw_ref)
    # Normaliser en minuscules pour les APIs (arXiv → arxiv)
    doi = doi_match.group(0).lower() if doi_match else None

    # Auto-extraire année et auteurs si non fournis
    if expected_year is None and expected_authors is None:
        expected_year, expected_authors = _extract_metadata_from_raw(raw_ref)

    # Extraire un titre propre pour la recherche fallback
    title_for_search = _extract_title(raw_ref)

    if doi:
        crossref, openalex, semantic = await asyncio.gather(
            query_crossref(doi=doi),
            query_openalex(doi=doi),
            query_semantic_scholar(doi=doi),
        )
        results = [r for r in [crossref, openalex, semantic] if r]

        # Fix 1: Si le DOI ne trouve rien, fallback par titre
        if not results and title_for_search:
            crossref, openalex, semantic = await asyncio.gather(
                query_crossref(title=title_for_search),
                query_openalex(title=title_for_search),
                query_semantic_scholar(title=title_for_search),
            )
            candidates = [r for r in [crossref, openalex, semantic] if r]
            # Filtrer les résultats dont le titre est trop différent du titre attendu
            results = [r for r in candidates if _title_matches(r.get("title"), title_for_search)]
    else:
        search_query = title_for_search or raw_ref
        crossref, openalex, semantic = await asyncio.gather(
            query_crossref(title=search_query),
            query_openalex(title=search_query),
            query_semantic_scholar(title=search_query),
        )
        candidates = [r for r in [crossref, openalex, semantic] if r]
        # Filtrer sur similarité titre uniquement si on a un titre extrait propre
        if title_for_search:
            results = [r for r in candidates if _title_matches(r.get("title"), title_for_search)]
        else:
            results = candidates

    if not results:
        return {
            "status": "not_found",
            "confidence": 0.0,
            "message": "Aucune source n'a trouvé cette référence.",
            "sources": [],
            "best_match": None,
        }

    best = _pick_best(results, expected_year)
    issues = _check_consistency(best, expected_year, expected_authors)

    confidence = _compute_confidence(results, issues)

    return {
        "status": "warning" if issues else "ok",
        "confidence": confidence,
        "message": "; ".join(issues) if issues else "Référence vérifiée.",
        "sources": [r["source"] for r in results],
        "best_match": best,
    }


def _title_matches(api_title: str | None, expected_title: str, threshold: float = 0.65) -> bool:
    """Vérifie que le titre retourné par l'API ressemble suffisamment au titre attendu.
    Utilise une similarité simple basée sur les mots communs (Jaccard)."""
    if not api_title or not expected_title:
        return False
    stop = {"the", "a", "an", "of", "in", "on", "for", "and", "or", "with", "is", "to", "at", "by"}
    api_words = {w.lower() for w in re.findall(r"\b\w+\b", api_title) if w.lower() not in stop and len(w) > 2}
    exp_words = {w.lower() for w in re.findall(r"\b\w+\b", expected_title) if w.lower() not in stop and len(w) > 2}
    if not exp_words:
        return True
    intersection = api_words & exp_words
    union = api_words | exp_words
    jaccard = len(intersection) / len(union) if union else 0
    return jaccard >= threshold


def _extract_title(raw_ref: str) -> str | None:
    """Extrait le titre depuis une référence brute (entre backticks LaTeX ou guillemets)."""
    # LaTeX: ``Title here''
    m = re.search(r"``(.+?)''", raw_ref)
    if m:
        return m.group(1).strip()
    # Guillemets doubles: "Title here"
    m = re.search(r'"([^"]{10,})"', raw_ref)
    if m:
        return m.group(1).strip()
    return None


def _pick_best(results: list[dict], expected_year: int = None) -> dict:
    # Priorité CrossRef > OpenAlex > Semantic Scholar
    priority = {"crossref": 0, "openalex": 1, "semantic_scholar": 2}
    ranked = sorted(results, key=lambda r: priority.get(r["source"], 99))
    best = ranked[0]

    # Si l'année du best est aberrante (> 5 ans d'écart), préférer une source plus fiable
    if expected_year and best.get("year"):
        if abs(best["year"] - expected_year) > 5:
            for r in ranked[1:]:
                if r.get("year") and abs(r["year"] - expected_year) <= 5:
                    # Garder l'abstract du best si disponible, mais utiliser la meilleure année
                    abstract = best.get("abstract") or r.get("abstract")
                    best = {**r, "abstract": abstract}
                    break

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
        diff = abs(match["year"] - expected_year)
        # Tolérance élargie pour les papiers arXiv dont les APIs retournent
        # l'année de la version récente (ex: 2025) plutôt que la publication originale.
        # Si l'écart > 3 ans mais expected_year est l'année d'un arXiv classique,
        # on vérifie si l'année API est plausible (pas > année courante).
        current_year = datetime.date.today().year
        api_year = match["year"]
        # Si l'API retourne une année récente (≤ 2 ans) pour un vieux papier (≥ 3 ans),
        # c'est un problème d'indexation de version, pas une erreur de l'auteur.
        api_is_recent = api_year >= current_year - 2   # 2024 ou 2025 en 2026
        paper_is_old = expected_year <= current_year - 3  # papier de 2023 ou avant
        if api_is_recent and paper_is_old:
            pass  # ne pas pénaliser
        elif diff > YEAR_TOLERANCE:
            issues.append(f"Année incorrecte : trouvé {api_year}, attendu {expected_year}")

    if expected_authors and match.get("authors"):
        found_families = {a.split()[-1].lower() for a in match["authors"] if a}
        expected_families = {a.split()[-1].lower() for a in expected_authors if a}
        missing = expected_families - found_families
        if missing:
            issues.append(f"Auteurs non trouvés : {', '.join(missing)}")

    return issues


def _compute_confidence(results: list[dict], issues: list[str]) -> float:
    base = min(len(results) / 3, 1.0)  # 0.33 / 0.66 / 1.0 selon nb de sources
    # Pénalité double si l'écart d'année est très grand (> 5 ans)
    year_issues = sum(1 for i in issues if "Année incorrecte" in i)
    author_issues = sum(1 for i in issues if "Auteurs" in i)
    penalty = year_issues * 0.2 + author_issues * 0.2
    return round(max(0.0, base - penalty), 2)
