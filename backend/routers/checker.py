from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import aiofiles
import os
import uuid
from pathlib import Path

from modules.parser import parse_file, extract_citing_sentences
from modules.reference_checker.verifier import verify_reference
from modules.reference_checker.semantic import compute_similarity
from modules.reference_checker.api_client import query_crossref, query_openalex

router = APIRouter(prefix="/checker", tags=["Reference Checker"])

UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


class ReferenceReport(BaseModel):
    cite_key: str
    raw_text: str
    verification: dict
    semantic: dict | None
    citing_sentences: list[str]


@router.post("/upload", summary="Upload un manuscrit et vérifie ses références")
async def upload_and_check(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".tex", ".docx", ".md", ".markdown"):
        raise HTTPException(status_code=400, detail=f"Format non supporté : {ext}")

    file_id = str(uuid.uuid4())
    save_path = str(UPLOAD_DIR / f"{file_id}{ext}")

    async with aiofiles.open(save_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    try:
        parsed = parse_file(save_path)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    reports = []
    for key in parsed["cite_keys"]:
        raw_bib = parsed["bibliography"].get(key, key)
        verification = await verify_reference(raw_bib)

        semantic_result = None
        best = verification.get("best_match")
        if best and best.get("abstract"):
            sentences = extract_citing_sentences(parsed["text"], key)
            if sentences:
                semantic_result = compute_similarity(sentences[0], best["abstract"])

        reports.append(
            ReferenceReport(
                cite_key=key,
                raw_text=raw_bib,
                verification=verification,
                semantic=semantic_result,
                citing_sentences=extract_citing_sentences(parsed["text"], key),
            )
        )

    summary = _build_summary(reports)

    return {
        "file_id": file_id,
        "format": parsed["format"],
        "total_references": len(reports),
        "summary": summary,
        "reports": [r.model_dump() for r in reports],
    }


@router.post("/verify-doi", summary="Vérifie un DOI unique")
async def verify_doi(doi: str):
    crossref = await query_crossref(doi=doi)
    openalex = await query_openalex(doi=doi)
    return {
        "doi": doi,
        "crossref": crossref,
        "openalex": openalex,
        "found": crossref is not None or openalex is not None,
    }


def _build_summary(reports: list[ReferenceReport]) -> dict:
    total = len(reports)
    ok = sum(1 for r in reports if r.verification["status"] == "ok")
    not_found = sum(1 for r in reports if r.verification["status"] == "not_found")
    warning = sum(1 for r in reports if r.verification["status"] == "warning")
    suspect_semantic = sum(
        1 for r in reports
        if r.semantic and r.semantic.get("label") == "suspect"
    )
    return {
        "ok": ok,
        "warning": warning,
        "not_found": not_found,
        "suspect_semantic": suspect_semantic,
        "hallucination_risk": not_found + suspect_semantic,
        "score": round(ok / total * 100, 1) if total else 0,
    }
