# -----------------------------
# SSL BYPASS
# -----------------------------
import os
import ssl
import urllib3

os.environ["HF_HUB_DISABLE_SSL_VERIFICATION"] = "1"
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["REQUESTS_CA_BUNDLE"] = ""

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -----------------------------
# IMPORTS
# -----------------------------
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from text_utils import normalize_text

# -----------------------------
# LOAD VECTOR DATABASE
# -----------------------------
index = faiss.read_index("vector_db/index.faiss")

with open("vector_db/texts.pkl", "rb") as f:
    texts = pickle.load(f)

# -----------------------------
# LOAD EMBEDDING MODEL (ONCE)
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# LIGHT FIR PREPROCESSING
# -----------------------------
def preprocess_fir(text: str) -> str:
    normalized = normalize_text(text)
    return normalized.lower()

# -----------------------------
# MAIN RETRIEVAL FUNCTION
# -----------------------------
def retrieve_sections(fir_text, top_k=5):

    # Normalize FIR
    fir_text = preprocess_fir(fir_text)

    if not fir_text:
        return []

    # Encode query
    query_embedding = model.encode([fir_text]).astype("float32")

    # Search more candidates so we can filter
    distances, indices = index.search(query_embedding, top_k * 3)

    max_distance = float(max(distances[0])) if max(distances[0]) != 0 else 1.0

    legal_results = []
    other_results = []

    for i, idx in enumerate(indices[0]):
        distance = float(distances[0][i])
        confidence = 1 - (distance / max_distance)

        text = texts[int(idx)]

        entry = {
            "section_text": text,
            "confidence": round(float(confidence), 2)
        }

        # Prioritize legal sections
        if "IPC" in text or "CrPC" in text:
            legal_results.append(entry)
        else:
            other_results.append(entry)

    # Select top results giving priority to IPC/CrPC
    final_results = legal_results[:top_k]

    if len(final_results) < top_k:
        final_results.extend(other_results[: top_k - len(final_results)])

    return final_results
