# -----------------------------
# IMPORTS
# -----------------------------
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
from uuid import uuid4
import logging
# CHANGED: add regex utilities for topic normalization
import re
# CHANGED: add fuzzy matching for near-duplicate topics
from difflib import SequenceMatcher

from rag_fir_engine import retrieve_sections
from pdf_ingest import ingest_uploaded_pdf
# CHANGED: reuse shared text normalization for consistent dedupe keys
from text_utils import normalize_text

# -----------------------------
# FASTAPI APP INITIALIZATION
# -----------------------------
app = FastAPI(
    title="AI Legal Assistant",
    description="AI-based FIR Analysis using IPC & CrPC",
    version="1.2"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_legal_assistant")

# CHANGED: normalize section text for deduplication comparisons
def _normalize_topic_text(value: str) -> str:
    # CHANGED: normalize using shared text cleanup
    text = normalize_text(value)
    # CHANGED: standardize casing for comparisons
    text = text.lower()
    # CHANGED: strip non-alphanumeric characters
    text = re.sub(r"[^a-z0-9]+", " ", text)
    # CHANGED: collapse whitespace for stable keys
    return re.sub(r"\s+", " ", text).strip()

# CHANGED: detect near-duplicate topics by normalized text similarity
def _is_near_duplicate(a: str, b: str) -> bool:
    # CHANGED: short-circuit empty comparisons
    if not a or not b:
        # CHANGED: treat empty strings as non-duplicates
        return False
    # CHANGED: exact match check
    if a == b:
        # CHANGED: exact matches are duplicates
        return True
    # CHANGED: containment check for minor variations
    if a in b or b in a:
        # CHANGED: containment indicates a near-duplicate
        return True
    # CHANGED: fallback to fuzzy similarity
    return SequenceMatcher(None, a, b).ratio() >= 0.92

# CHANGED: deduplicate and merge sections before display
def dedupe_sections(sections):
    # CHANGED: prepare merged output structure
    merged = []
    # CHANGED: handle None safely
    for entry in sections or []:
        # CHANGED: read section text defensively
        text = entry.get("section_text", "")
        # CHANGED: build normalized key for matching
        norm = _normalize_topic_text(text)
        # CHANGED: skip empty keys
        if not norm:
            # CHANGED: continue to next entry if no usable text
            continue
        # CHANGED: find an existing near-duplicate
        match = None
        # CHANGED: scan merged entries in order to preserve ranking
        for existing in merged:
            # CHANGED: compare normalized text for duplication
            if _is_near_duplicate(norm, existing["_norm"]):
                # CHANGED: mark the duplicate match
                match = existing
                # CHANGED: stop after first match
                break
        # CHANGED: parse confidence safely as float
        confidence = float(entry.get("confidence", 0) or 0)
        # CHANGED: merge with existing match when found
        if match:
            # CHANGED: accumulate confidence for averaging
            match["confidence_sum"] += confidence
            # CHANGED: increment merge count
            match["confidence_count"] += 1
            # CHANGED: keep the most informative text variant
            if len(text) > len(match["section_text"]):
                # CHANGED: update to longer section text
                match["section_text"] = text
                # CHANGED: update normalized key to match kept text
                match["_norm"] = norm
        # CHANGED: add a new unique section entry
        else:
            # CHANGED: store merged entry with tracking fields
            merged.append({
                # CHANGED: keep original section text
                "section_text": text,
                # CHANGED: track total confidence for averaging
                "confidence_sum": confidence,
                # CHANGED: track count for averaging
                "confidence_count": 1,
                # CHANGED: store normalized text for comparisons
                "_norm": norm
                # CHANGED: close merged entry definition
            })
    # CHANGED: finalize merged results for response payload
    results = []
    # CHANGED: compute averaged confidence for each merged entry
    for existing in merged:
        # CHANGED: avoid divide-by-zero while averaging confidence
        avg_conf = existing["confidence_sum"] / existing["confidence_count"] if existing["confidence_count"] else 0.0
        # CHANGED: append cleaned output with averaged confidence
        results.append({
            # CHANGED: keep selected section text
            "section_text": existing["section_text"],
            # CHANGED: round confidence for UI consistency
            "confidence": round(avg_conf, 2)
            # CHANGED: close result entry definition
        })
    # CHANGED: return deduplicated sections
    return results

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FIRRequest(BaseModel):
    fir_text: str

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("frontend.html", "r", encoding="utf-8") as f:
        return f.read()

# -----------------------------
# PDF UPLOAD
# -----------------------------
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf", "application/x-pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    safe_name = Path(file.filename).name or f"upload_{uuid4().hex}.pdf"
    file_path = os.path.join(UPLOAD_DIR, f"{uuid4().hex}_{safe_name}")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = ingest_uploaded_pdf(file_path)
        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail="No extractable text found in the PDF (scanned image or empty file)."
            )

        # CHANGED: retrieve sections using the same pipeline as manual input
        sections = retrieve_sections(extracted_text)
        # CHANGED: deduplicate sections before downstream counts and display
        sections = dedupe_sections(sections)
    except ValueError as exc:
        logger.exception("PDF processing failed: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        await file.close()

    # safer IPC/CrPC counting
    ipc_sections = []
    crpc_sections = []

    for s in sections:
        if "IPC" in s["section_text"]:
            ipc_sections.append(s["section_text"].split("\n")[0])
        if "CrPC" in s["section_text"]:
            crpc_sections.append(s["section_text"].split("\n")[0])

    if ipc_sections:
        summary = (
            "Based on the uploaded FIR document, the alleged incident appears to involve "
            + ", ".join(ipc_sections[:2])
            + ". These provisions indicate the presence of cognizable criminal acts. "
        )
    else:
        summary = "Based on the uploaded document, no specific IPC offences could be conclusively identified. "

    if crpc_sections:
        summary += (
            "Relevant procedural provisions such as "
            + ", ".join(crpc_sections[:2])
            + " may apply during the investigation process."
        )

    k = 5
    total_relevant = len(ipc_sections) + len(crpc_sections)
    precision_at_k = round(total_relevant / k, 2) if sections else 0.0
    recall_at_k = round(min(total_relevant, 3) / 3, 2) if total_relevant else 0.0
    accuracy = round((precision_at_k + recall_at_k) / 2, 2)

    return {
        "summary": summary,
        "sections": sections,
        "ipc_count": len(ipc_sections),
        "crpc_count": len(crpc_sections),
        "precision": precision_at_k,
        "recall": recall_at_k,
        "accuracy": accuracy
    }

# -----------------------------
# TEXT FIR
# -----------------------------
@app.post("/analyze_fir")
def analyze_fir(req: FIRRequest):

    # CHANGED: retrieve sections using the same pipeline as PDF input
    sections = retrieve_sections(req.fir_text)
    # CHANGED: deduplicate sections before downstream counts and display
    sections = dedupe_sections(sections)

    ipc_sections = []
    crpc_sections = []

    for s in sections:
        if "IPC" in s["section_text"]:
            ipc_sections.append(s["section_text"].split("\n")[0])
        if "CrPC" in s["section_text"]:
            crpc_sections.append(s["section_text"].split("\n")[0])

    if ipc_sections:
        summary = (
            "Based on the contents of the FIR, the alleged incident appears to involve "
            + ", ".join(ipc_sections[:2])
            + ". These provisions indicate the presence of cognizable criminal acts. "
        )
    else:
        summary = "Based on the FIR description, no specific IPC offences could be conclusively identified. "

    if crpc_sections:
        summary += (
            "Relevant procedural provisions such as "
            + ", ".join(crpc_sections[:2])
            + " may apply during the investigation process."
        )

    k = 5
    total_relevant = len(ipc_sections) + len(crpc_sections)
    precision_at_k = round(total_relevant / k, 2) if sections else 0.0
    recall_at_k = round(min(total_relevant, 3) / 3, 2) if total_relevant else 0.0
    accuracy = round((precision_at_k + recall_at_k) / 2, 2)

    return {
        "summary": summary,
        "sections": sections,
        "ipc_count": len(ipc_sections),
        "crpc_count": len(crpc_sections),
        "precision": precision_at_k,
        "recall": recall_at_k,
        "accuracy": accuracy
    }
