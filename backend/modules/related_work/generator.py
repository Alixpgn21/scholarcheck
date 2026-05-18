"""
Génération de la section Related Work.
Implémente la boucle Self-Refine (Phase 4) et le support multi-LLM (Phase 6).
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
        return _generate_with_llm(clusters, embeddings, all_documents, topic)
    except Exception as e:
        print(f"LLM Generation fallback: {e}")
        return _generate_template(clusters, embeddings, all_documents, topic)


def _call_llm(prompt: str) -> str:
    from config import (
        ANTHROPIC_API_KEY, OPENAI_API_KEY, 
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    )
    
    # 1. AWS Bedrock (API Converse unifiée pour Anthropic, Llama, Nova, Mistral)
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        import boto3
        from config import AWS_BEDROCK_MODEL_ID
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        
        response = bedrock.converse(
            modelId=AWS_BEDROCK_MODEL_ID,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 2048, "temperature": 0.2}
        )
        return response['output']['message']['content'][0]['text']
        
    # 2. Anthropic API
    elif ANTHROPIC_API_KEY:
        from anthropic import Anthropic
        client = Anthropic(api_key=ANTHROPIC_API_KEY)
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.content[0].text
        
    # 3. OpenAI API
    elif OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message.content
        
    # 4. Fallback Ollama Local
    else:
        resp = httpx.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["response"]


def _generate_with_llm(
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

    # ÉTAPE 1 : Génération Initiale (Draft)
    draft_prompt = f"""You are an expert academic writer. Write a "Related Work" section for a paper on: {topic}.

Available documents grouped by theme:
{corpus_context}

STRICT rules:
1. Cite every claim with [Paper Title] from the corpus above.
2. Do NOT invent references.
3. One paragraph per theme group.
4. Write in academic English.

Write the Related Work section:"""
    
    draft_text = _call_llm(draft_prompt)
    
    # ÉTAPE 2 : Boucle Self-Refine
    refine_prompt = f"""Review the following "Related Work" draft against the provided source corpus.
Your goal is to detect and remove ANY claim or citation in the draft that is NOT explicitly supported by the corpus.

CORPUS:
{corpus_context}

DRAFT:
{draft_text}

Task: Rewrite the DRAFT to fix any hallucinations. If a claim is not in the corpus, remove it.
Return ONLY the final corrected academic text."""

    refined_text = _call_llm(refine_prompt)
    
    return refined_text


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
