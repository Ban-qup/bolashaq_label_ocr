"""Central place for all regex / validation patterns used by the OCR pipeline."""

import re

# Example pattern: two or three letters, optional dash, 3–6 digits (e.g., SL-1234, L09876)
SERIAL_PATTERN = re.compile(r"[A-ZА-Я]{1,3}-?\d{3,6}")

def filter_matches(raw_text: str):
    """Return first match that fits the pattern or empty string."""
    m = SERIAL_PATTERN.search(raw_text.upper())
    return m.group(0) if m else ""
