# CHANGED: add regex for PDF text normalization checks
import re
# CHANGED: keep PDF reader import
from pypdf import PdfReader
# CHANGED: reuse shared normalization to align PDF text with manual input flow
from text_utils import normalize_text

def ingest_uploaded_pdf(file_path):
    # CHANGED: guard against malformed or unreadable PDFs
    try:
        # CHANGED: keep PdfReader strict mode aligned with current behavior
        reader = PdfReader(file_path, strict=False)
    # CHANGED: surface a user-friendly error for malformed PDFs
    except Exception as exc:
        # CHANGED: propagate a ValueError that the API layer already handles
        raise ValueError("Malformed or unreadable PDF file") from exc

    if getattr(reader, "is_encrypted", False):
        try:
            reader.decrypt("")
        except Exception as exc:
            raise ValueError("Encrypted PDF cannot be processed") from exc

    # CHANGED: collect per-page text with lightweight extraction error handling
    page_texts = []
    # CHANGED: iterate through pages defensively
    for page in reader.pages:
        # CHANGED: handle per-page extraction failures without crashing the upload
        try:
            # CHANGED: extract text if possible, otherwise use empty string
            page_text = page.extract_text() or ""
        # CHANGED: treat extract_text failures as empty text for the page
        except Exception:
            # CHANGED: ensure page_text is always a string
            page_text = ""
        # CHANGED: append the extracted page text
        page_texts.append(page_text)

    # CHANGED: join pages to preserve paragraph breaks
    text = "\n\n".join(page_texts)
    # CHANGED: normalize PDF artifacts (nulls, hyphenation, whitespace)
    text = normalize_text(text)
    # CHANGED: collapse single line breaks to match manual input flow
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    # CHANGED: re-normalize after line break collapsing
    text = normalize_text(text)
    # CHANGED: treat PDFs with no meaningful text as empty for upstream handling
    if not text or not re.search(r"[A-Za-z0-9]", text):
        # CHANGED: return empty string to trigger existing 422 handling
        return ""

    # CHANGED: return cleaned text for the standard processing pipeline
    return text
