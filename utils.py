from datetime import datetime
from pathlib import Path

def list_images(folder: Path):
    """Yield image files with common extensions."""
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff"):
        yield from folder.glob(ext)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
