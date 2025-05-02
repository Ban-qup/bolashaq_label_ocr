# Bolashaq Label OCR Tool

Lightweight, fully open‑source tool to extract serial numbers or text labels
from photos of street‑lighting equipment. Designed during the 2025 Astana IT University
industrial internship at **Bolashaq Energıasy LLP**.

## Features
* Pure‑Python stack (no GPU, no paid cloud)
* Image pre‑processing (rotation, CLAHE, denoise, binarisation)
* Text recognition via Tesseract‑OCR
* Post‑processing with a regex pattern (`SL‑1234`, `L‑09876`, etc.)
* Tkinter GUI (`python gui_app.py`) and CLI batch mode (`python main.py folder/`)

## Quick start

```bash
# 1. Create venv (optional)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows

# 2. Install deps
pip install -r requirements.txt

# 3. Run GUI
python gui_app.py
```

*Tesseract* must be installed separately
(Windows installer: https://github.com/tesseract-ocr/tesseract/wiki).
Add the binary folder to your `PATH`.

## Directory structure
```
bolashaq_label_ocr/
├── gui_app.py
├── main.py
├── ocr.py
├── preprocess.py
├── utils.py
├── patterns.py
├── requirements.txt
└── README.md
```
