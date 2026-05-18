"""
Génération de la section Related Work.
Stratégie : Ollama (local, gratuit) si disponible, sinon template-based.
"""
import httpx
import json
from .clustering import get_cluster_representatives
import numpy as np


def generate_related_work(
    clusters: list[dict],
    embeddings: np.ndarray,
    all_documents: list[dict],
    topic: str = "ce sujet de recherche",
) -> str:
    try:
        return _generate_with_ollama(clusters, embeddings, all_documents, topic)
    except Exception:
        return _generate_template(clusters, embeddings, all_documents, topic)


def _generate_with_ollama(
    clusters: list[dict],
    embeddings: np.ndarray,
    all_documents: list[dict],
    topic: str,
) -> str:
    cluster_summaries = []
    for cluster in clusters:
        reps = get_cluster_representatives(cluster, embeddings, all_documents, top_k=3)
        docs_text = "\n".join(
            f"- [{d.get('title', 'Sans titre')}] ({d.get('year', '?')}) — {(d.get('abstract') or '')[:250]}"
            for d in reps
        )
        cluster_summaries.append(f"### {cluster['label']}\n{docs_text}")

    corpus_context = "\n\n".join(cluster_summaries)

    prompt = f"""You are an expert academic writer. Write a "Related Work" section for a paper on: {topic}.

Available documents grouped by theme:
{corpus_context}

STRICT rules:
1. Cite every claim with [Paper Title] from the corpus above.
2. Do NOT invent references.
3. One paragraph per theme group.
4. Write in academic English (IEEE/NeurIPS style).
5. Start directly with the text.

Write the Related Work section:"""

    resp = httpx.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["response"]


def _generate_template(
    clusters: list[dict],
    embeddings: np.ndarray,
    all_documents: list[dict],
    topic: str,
) -> str:
    """Génère une Related Work structurée sans LLM — 100% déterministe."""
    paragraphs = []

    intro = (
        f"This section reviews the existing literature related to {topic}. "
        f"We identify {len(clusters)} main research directions in the corpus."
    )
    paragraphs.append(intro)

    transition_phrases = [
        "A significant body of work has focused on",
        "Several studies have investigated",
        "Recent research has examined",
        "An important line of inquiry concerns",
        "Considerable attention has been devoted to",
    ]

    for idx, cluster in enumerate(clusters):
        reps = get_cluster_representatives(cluster, embeddings, all_documents, top_k=5)
        if not reps:
            continue

        transition = transition_phrases[idx % len(transition_phrases)]
        titles_block = ", ".join(
            f"[{d.get('title', 'Untitled')}]" for d in reps
        )

        sentences = [f"{transition} this research theme ({titles_block})."]

        for doc in reps:
            title = doc.get("title", "Untitled")
            year = doc.get("year", "n.d.")
            abstract = doc.get("abstract") or ""

            if abstract:
                snippet = abstract[:200].rstrip()
                if not snippet.endswith("."):
                    snippet += "..."
                sentences.append(f"[{title}] ({year}) reports that {snippet.lower()}")
            else:
                sentences.append(
                    f"[{title}] ({year}) contributes to this direction with relevant findings."
                )

        paragraphs.append(" ".join(sentences))

    closing = (
        "Taken together, these works establish the foundation upon which the present study builds, "
        "highlighting gaps that motivate our proposed approach."
    )
    paragraphs.append(closing)

    return "\n\n".join(paragraphs)
