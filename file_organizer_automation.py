from __future__ import annotations

import argparse
import datetime
import logging
import shutil
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
sys.stdout.reconfigure(encoding="utf-8")

# Map each file category to the extensions that belong to it.
categories: dict[str, list[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".aac"],
}


def create_destination(base: Path, file_type_folder: str, date_folder: str) -> Path:
    """Create the full destination folder path and ensure it exists."""
    destination = base / file_type_folder / date_folder
    destination.mkdir(parents=True, exist_ok=True)
    return destination


def get_file_category(extension: str) -> str:
    """Return the category name for a given file extension."""
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    return "Others"


def get_date_folder(file_path: Path) -> str:
    """Build a folder name from the file's modification date, such as 2026-July."""
    timestamp = file_path.stat().st_mtime
    date = datetime.datetime.fromtimestamp(timestamp)
    return f"{date.year}-{date.strftime('%B')}"


def organize_files(folder: Path, dry_run: bool = False) -> list[dict[str, Any]]:
    """Move files into category/date-based folders.

    Each file is grouped by its type and by the month from its modification date.
    If a target file already exists, the script renames the incoming file so it
    does not overwrite the existing one.
    """
    results: list[dict[str, Any]] = []
    known_categories = {"Images", "Documents", "Videos", "Music", "Others"}

    for file in folder.glob("*"):
        # Skip the folders created by this tool so it does not reorganize its own output.
        if file.name in known_categories:
            continue

        if file.is_file():
            extension = file.suffix.lower()
            category = get_file_category(extension)
            date = get_date_folder(file)
            destination = create_destination(folder, category, date)

            safe_destination = destination / file.name
            counter = 1
            while safe_destination.exists():
                safe_destination = destination / f"{file.stem} ({counter}){file.suffix}"
                counter += 1

            if dry_run:
                results.append(
                    {
                        "file": file.name,
                        "destination": str(safe_destination),
                        "status": "would_move",
                    }
                )
            else:
                try:
                    shutil.move(file, safe_destination)
                    results.append(
                        {
                            "file": file.name,
                            "destination": str(safe_destination),
                            "status": "moved",
                        }
                    )
                except Exception as exc:
                    results.append(
                        {
                            "file": file.name,
                            "destination": None,
                            "status": "error",
                            "error": str(exc),
                        }
                    )

    return results


def main() -> None:
    """Parse command-line arguments and organize the selected folders."""
    parser = argparse.ArgumentParser(description="Organize files into category/date folders")
    parser.add_argument("--folder", default=None, help="Folder to organize")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files",
    )
    args = parser.parse_args()

    if args.folder:
        results = organize_files(Path(args.folder), dry_run=args.dry_run)
    else:
        results = organize_files(Path.home() / "Downloads", dry_run=args.dry_run) + organize_files(
            Path.home() / "Desktop", dry_run=args.dry_run
        )

    for result in results:
        if result["status"] == "moved":
            logging.info(f"Moved: {result['file']} -> {result['destination']}")
        elif result["status"] == "would_move":
            logging.info(f"[DRY RUN] Would move: {result['file']} -> {result['destination']}")
        else:
            logging.error(f"Skipped {result['file']}: {result['error']}")

    logging.info("Done! Your folders are organized.")


if __name__ == "__main__":
    main()