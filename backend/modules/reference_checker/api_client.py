"""
Clients pour CrossRef, OpenAlex et Semantic Scholar.
"""
import httpx
from .cache import cached_api_call
from config import (
    CROSSREF_BASE_URL,
    OPENALEX_BASE_URL,
    SEMANTIC_SCHOLAR_BASE_URL,
    CROSSREF_EMAIL,
    SEMANTIC_SCHOLAR_API_KEY,
)


@cached_api_call
async def query_crossref(title: str = None, doi: str = None) -> dict | None:
    params = {"mailto": CROSSREF_EMAIL}
    async with httpx.AsyncClient(timeout=10) as client:
        if doi:
            resp = await client.get(f"{CROSSREF_BASE_URL}/{doi}", params=params)
        elif title:
            params["query.title"] = title
            params["rows"] = 1
            resp = await client.get(CROSSREF_BASE_URL, params=params)
        else:
            return None

        if resp.status_code != 200:
            return None

        data = resp.json()
        if doi:
            item = data.get("message", {})
        else:
            items = data.get("message", {}).get("items", [])
            item = items[0] if items else {}

        if not item:
            return None

        return {
            "source": "crossref",
            "doi": item.get("DOI"),
            "title": _first(item.get("title")),
            "authors": _format_authors(item.get("author", [])),
            "year": _extract_year(item),
            "abstract": item.get("abstract"),
            "url": item.get("URL"),
        }


@cached_api_call
async def query_openalex(title: str = None, doi: str = None) -> dict | None:
    async with httpx.AsyncClient(timeout=10) as client:
        if doi:
            resp = await client.get(f"{OPENALEX_BASE_URL}/https://doi.org/{doi}")
        elif title:
            resp = await client.get(
                OPENALEX_BASE_URL,
                params={"search": title, "per-page": 1},
            )
        else:
            return None

        if resp.status_code != 200:
            return None

        data = resp.json()
        if doi:
            item = data
        else:
            results = data.get("results", [])
            item = results[0] if results else {}

        if not item:
            return None

        abstract = _reconstruct_abstract(item.get("abstract_inverted_index"))
        authors = [
            a.get("author", {}).get("display_name", "")
            for a in item.get("authorships", [])
        ]

        return {
            "source": "openalex",
            "doi": item.get("doi", "").replace("https://doi.org/", ""),
            "title": item.get("title"),
            "authors": authors,
            "year": item.get("publication_year"),
            "abstract": abstract,
            "url": item.get("id"),
            "openalex_id": item.get("id"),
            "referenced_works": item.get("referenced_works", []),
        }


@cached_api_call
async def query_semantic_scholar(title: str = None, doi: str = None) -> dict | None:
    headers = {}
    if SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY

    async with httpx.AsyncClient(timeout=10, headers=headers) as client:
        if doi:
            resp = await client.get(
                f"{SEMANTIC_SCHOLAR_BASE_URL}/paper/DOI:{doi}",
                params={"fields": "title,authors,year,abstract,externalIds"},
            )
        elif title:
            resp = await client.get(
                f"{SEMANTIC_SCHOLAR_BASE_URL}/paper/search",
                params={"query": title, "limit": 1, "fields": "title,authors,year,abstract,externalIds"},
            )
        else:
            return None

        if resp.status_code != 200:
            return None

        data = resp.json()
        if doi:
            item = data
        else:
            items = data.get("data", [])
            item = items[0] if items else {}

        if not item:
            return None

        return {
            "source": "semantic_scholar",
            "doi": item.get("externalIds", {}).get("DOI"),
            "title": item.get("title"),
            "authors": [a.get("name") for a in item.get("authors", [])],
            "year": item.get("year"),
            "abstract": item.get("abstract"),
            "url": f"https://www.semanticscholar.org/paper/{item.get('paperId', '')}",
        }


# Helpers
def _first(lst):
    return lst[0] if lst else None


def _format_authors(author_list: list) -> list[str]:
    result = []
    for a in author_list:
        given = a.get("given", "")
        family = a.get("family", "")
        result.append(f"{given} {family}".strip())
    return result


def _extract_year(item: dict) -> int | None:
    date_parts = item.get("published", {}).get("date-parts", [[]])
    if date_parts and date_parts[0]:
        return date_parts[0][0]
    return None


def _reconstruct_abstract(inverted_index: dict | None) -> str | None:
    if not inverted_index:
        return None
    words = {}
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words[i] for i in sorted(words))
