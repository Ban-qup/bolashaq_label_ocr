"""Image loading and pre‑processing utilities."""
import cv2
import numpy as np
from pathlib import Path

def _apply_clahe(gray):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)

def preprocess_image(path: Path):
    """Load image file and return a pre‑processed numpy array suitable for OCR."""
    img = cv2.imread(str(path))
    if img is None:
        raise FileNotFoundError(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Simple orientation fix: if width > height * 1.2 assume landscape and rotate
    h, w = gray.shape
    if w > h * 1.2:
        gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)

    gray = _apply_clahe(gray)

    # Denoise & threshold
    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    _, th = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th
