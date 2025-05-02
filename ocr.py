"""Wrapper around pytesseract with post‑processing."""
from pathlib import Path
import pytesseract
from PIL import Image
from preprocess import preprocess_image
from patterns import filter_matches

TESS_CONFIG = "--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"


def extract_label(image_path: Path) -> str:
    """Return validated label string or empty string if nothing found."""
    pre = preprocess_image(image_path)
    pil_img = Image.fromarray(pre)
    raw = pytesseract.image_to_string(pil_img, config=TESS_CONFIG)
    return filter_matches(raw)
