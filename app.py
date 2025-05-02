from __future__ import annotations

import argparse
import csv
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

from ocr import extract_label
from utils import list_images, timestamp

LOGGER = logging.getLogger("bolashaq.app")


# ---------------------------------------------------------------------------#
# Configuration                                                               #
# ---------------------------------------------------------------------------#
@dataclass(slots=True, frozen=True)
class AppConfig:
    input_path: Path
    output_path: Path | None
    recursive: bool
    verbose: bool

    def files(self) -> Iterable[Path]:
        """Yield image files according to config (recursive vs non‑recursive)."""
        if self.input_path.is_file():
            yield self.input_path
        else:
            patterns = ("**/*" if self.recursive else "*")
            for ext in (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"):
                yield from self.input_path.glob(f"{patterns}{ext}")


# ---------------------------------------------------------------------------#
# Core processing                                                             #
# ---------------------------------------------------------------------------#
def process_files(files: Iterable[Path]) -> List[Tuple[str, str]]:
    """Run OCR on a list of files, returning (filename, label) tuples."""
    results: List[Tuple[str, str]] = []
    for path in files:
        try:
            LOGGER.debug("Processing %s", path)
            label = extract_label(path)
            LOGGER.info("%s -> %s", path.name, label or "<no‑match>")
            results.append((path.name, label))
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.error("Failed to process %s: %s", path, exc, exc_info=LOGGER.level <= logging.DEBUG)
            results.append((path.name, "ERROR"))
    return results


def save_csv(rows: List[Tuple[str, str]], out_path: Path) -> None:
    """Write results to CSV with UTF‑8 BOM for Excel compatibility."""
    LOGGER.debug("Writing CSV to %s", out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["filename", "label"])
        writer.writerows(rows)
    LOGGER.info("CSV saved: %s (%d rows)", out_path, len(rows))


# ---------------------------------------------------------------------------#
# CLI                                                                        #
# ---------------------------------------------------------------------------#
def parse_args(argv: List[str]) -> AppConfig:
    parser = argparse.ArgumentParser(
        description="Bolashaq Label‑OCR — batch serial‑number extractor",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input", help="Image file or folder with images")  # positional
    parser.add_argument(
        "-o","--output", help="Optional CSV output (default: results_<timestamp>.csv)"
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recurse into sub‑folders"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")

    ns = parser.parse_args(argv)
    out = Path(ns.output) if ns.output else None
    cfg = AppConfig(
        input_path=Path(ns.input).expanduser(),
        output_path=out,
        recursive=ns.recursive,
        verbose=ns.verbose,
    )
    return cfg


def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="[%(levelname).1s] %(asctime)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    LOGGER.debug("Logging initialised at level %s", logging.getLevelName(level))


def main(argv: List[str] | None = None) -> None:
    cfg = parse_args(argv or sys.argv[1:])
    configure_logging(cfg.verbose)

    if not cfg.input_path.exists():
        LOGGER.error("Input path does not exist: %s", cfg.input_path)
        sys.exit(1)

    files = list(cfg.files())
    if not files:
        LOGGER.warning("No images found in %s", cfg.input_path)
        sys.exit(0)

    LOGGER.info("Found %d image(s)", len(files))
    results = process_files(files)

    if cfg.output_path is None:
        default_name = f"results_{timestamp()}.csv"
        cfg = cfg.__class__(
            input_path=cfg.input_path,
            output_path=Path(default_name),
            recursive=cfg.recursive,
            verbose=cfg.verbose,
        )

    save_csv(results, cfg.output_path)
    LOGGER.info("Finished.")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------#
# Diagnostics utilities (optionally imported by unit tests)                  #
# ---------------------------------------------------------------------------#
def success_rate(rows: List[Tuple[str, str]]) -> float:
    """Return percentage of rows where label is not empty and not 'ERROR'."""
    total = len(rows)
    if total == 0:
        return 0.0
    good = sum(1 for _, label in rows if label and label != "ERROR")
    return 100.0 * good / total


def print_summary(rows: List[Tuple[str, str]]) -> None:
    """Human‑friendly summary of batch run."""
    rate = success_rate(rows)
    LOGGER.info("Summary: %d of %d images produced non‑empty labels (%.1f%%)", len(rows), len(rows), rate)
    errors = [f for f, label in rows if label == "ERROR"]
    if errors:
        LOGGER.warning("%d file(s) failed: %s", len(errors), ", ".join(errors[:5]))
