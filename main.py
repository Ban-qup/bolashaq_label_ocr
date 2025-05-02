import argparse
from pathlib import Path
from ocr import extract_label
from utils import list_images

def main():
    parser = argparse.ArgumentParser(description="Batch label OCR for Bolashaq.")
    parser.add_argument("input", help="Folder with images or single image file")
    parser.add_argument("--save", metavar="OUTPUT", help="Optional CSV output path")
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        parser.error(f"Input path {in_path} does not exist")

    images = [in_path] if in_path.is_file() else list(list_images(in_path))
    if not images:
        print("No images found."); return

    results = []
    for img in images:
        label = extract_label(img)
        print(f"{img.name}: {label}")
        results.append((img.name, label))

    if args.save:
        import csv
        out = Path(args.save)
        with out.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["filename", "label"])
            writer.writerows(results)
        print(f"Saved CSV to {out}")

if __name__ == "__main__":
    main()
