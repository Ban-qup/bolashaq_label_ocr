"""
preprocess_pipeline.py — extended image processing utilities.
"""

from __future__ import annotations

from pathlib import Path
import cv2, numpy as np


class PipelineError(Exception):
    pass


class ImagePipeline:

    """Chainable image-processing pipeline object."""

    def __init__(self, img: np.ndarray):

        self.img = img

        self._history: list[str] = []


    def rotate_to_upright(self):

        h, w = self.img.shape[:2]

        if w > h * 1.2:
            self.img = cv2.rotate(self.img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self._history.append('rotate')
        return self


    def clahe(self, clip: float = 2.0):

        clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(8, 8))

        gray = self.img if len(self.img.shape) == 2 else cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        self.img = clahe.apply(gray)

        self._history.append(f'clahe_{clip}')
        return self


    def denoise(self):
        self.img = cv2.fastNlMeansDenoising(self.img, None, 30, 7, 21)
        self._history.append('denoise')
        return self


    def otsu_threshold(self):

        _, th = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        self.img = th
        self._history.append('otsu')
        return self


    def downscale(self, max_side: int = 1600):

        h, w = self.img.shape[:2]
        if max(h, w) > max_side:
            scale = max_side / max(h, w)
            self.img = cv2.resize(self.img, dsize=None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            self._history.append(f'down_{max_side}')
        return self


    def run(self):
        return self.img


def preprocess_image(path: Path) -> np.ndarray:

    src = cv2.imread(str(path))
    if src is None:
        raise PipelineError(f'Could not read {path}')

    pipeline = (
        ImagePipeline(src)
        .rotate_to_upright()
        .clahe()
        .denoise()
        .otsu_threshold()
        .downscale()
    )
    return pipeline.run()


# --- demo usage if run standalone ---

if __name__ == '__main__':

    import sys
    out_dir = Path('preview')
    out_dir.mkdir(exist_ok=True)

    for img_path in map(Path, sys.argv[1:]):

        try:
            processed = preprocess_image(img_path)
            cv2.imwrite(str(out_dir / img_path.name), processed)
            print(f'Saved {img_path.name}')
        except PipelineError as e:
            print(e)
