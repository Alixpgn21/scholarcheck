from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import aiofiles
import os
import uuid
import json
from pathlib import Path

from modules.parser import parse_file
from modules.reference_checker.api_client import query_openalex, query_semantic_scholar
from modules.related_work.embeddings import embed_documents
from modules.related_work.clustering import cluster_documents
from modules.related_work.generator import generate_related_work

router = APIRouter(prefix="/related-work", tags=["Related Work Generator"])

UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/generate", summary="Génère une section Related Work depuis un corpus")
async def generate_from_corpus(
    files: list[UploadFile] = File(...),
    topic: str = Form("ce sujet de recherche"),
):
    if not files:
        raise HTTPException(status_code=400, detail="Au moins un fichier requis.")

    documents = []

    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in (".tex", ".docx", ".md", ".markdown"):
            continue

        file_id = str(uuid.uuid4())
        save_path = str(UPLOAD_DIR / f"{file_id}{ext}")
        async with aiofiles.open(save_path, "wb") as f:
            await f.write(await file.read())

        try:
            parsed = parse_file(save_path)
        except Exception:
            continue

        # Enrichissement via OpenAlex ou Semantic Scholar
        meta = await query_openalex(title=file.filename.replace(ext, ""))
        if not meta:
            meta = await query_semantic_scholar(title=file.filename.replace(ext, ""))

        documents.append({
            "id": file_id,
            "filename": file.filename,
            "title": (meta or {}).get("title") or file.filename,
            "abstract": (meta or {}).get("abstract") or parsed["text"][:500],
            "authors": (meta or {}).get("authors", []),
            "year": (meta or {}).get("year"),
            "doi": (meta or {}).get("doi"),
            "openalex_id": (meta or {}).get("openalex_id"),
            "referenced_works": (meta or {}).get("referenced_works", []),
        })

    if not documents:
        raise HTTPException(status_code=422, detail="Aucun document valide dans le corpus.")

    embeddings = embed_documents(documents)
    clusters = cluster_documents(embeddings, documents)
    related_work_text = generate_related_work(clusters, embeddings, documents, topic=topic)

    return {
        "topic": topic,
        "document_count": len(documents),
        "cluster_count": len(clusters),
        "clusters": [
            {
                "id": c["cluster_id"],
                "label": c["label"],
                "documents": [{"title": d["title"], "year": d["year"]} for d in c["documents"]],
            }
            for c in clusters
        ],
        "related_work": related_work_text,
    }


@router.post("/generate-from-dois", summary="Génère une Related Work depuis une liste de DOIs")
async def generate_from_dois(payload: dict):
    """
    payload: {"dois": ["10.xxxx/...", ...], "topic": "..."}
    """
    dois = payload.get("dois", [])
    topic = payload.get("topic", "ce sujet de recherche")

    if not dois:
        raise HTTPException(status_code=400, detail="Liste de DOIs vide.")

    documents = []
    for doi in dois:
        meta = await query_openalex(doi=doi)
        if not meta:
            meta = await query_semantic_scholar(doi=doi)
        if meta:
            documents.append({
                "id": doi,
                "title": meta.get("title", doi),
                "abstract": meta.get("abstract", ""),
                "authors": meta.get("authors", []),
                "year": meta.get("year"),
                "doi": doi,
                "openalex_id": meta.get("openalex_id"),
                "referenced_works": meta.get("referenced_works", []),
            })

    if not documents:
        raise HTTPException(status_code=422, detail="Aucun DOI résolu.")

    embeddings = embed_documents(documents)
    clusters = cluster_documents(embeddings, documents)
    related_work_text = generate_related_work(clusters, embeddings, documents, topic=topic)

    return {
        "topic": topic,
        "document_count": len(documents),
        "cluster_count": len(clusters),
        "clusters": [
            {
                "id": c["cluster_id"],
                "label": c["label"],
                "documents": [{"title": d["title"], "year": d["year"]} for d in c["documents"]],
            }
            for c in clusters
        ],
        "related_work": related_work_text,
    }
