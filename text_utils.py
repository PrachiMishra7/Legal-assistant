import re
from typing import Any


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)

    text = value.replace("\x00", " ").replace("\u00a0", " ")
    text = text.replace("\r", "\n")

    # Fix common PDF hyphenation across line breaks: "com-\nplainant" -> "complainant"
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
