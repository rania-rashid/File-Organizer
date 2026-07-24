from pathlib import Path
import datetime
import shutil
import argparse
import logging
import sys
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
sys.stdout.reconfigure(encoding="utf-8")

categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".aac"]
}

def create_destination(base, file_type_folder, date_folder):
    destination = base / file_type_folder / date_folder
    destination.mkdir(parents=True, exist_ok=True)
    return destination

def get_file_category(extension):
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    return "Others"

def get_date_folder(file_path):
    timestamp = file_path.stat().st_mtime
    date = datetime.datetime.fromtimestamp(timestamp)
    return f"{date.year}-{date.strftime('%B')}"

def organize_files(folder, dry_run=False):
    results = []
    known_categories = ["Images", "Documents", "Videos", "Music", "Others"]
    for file in folder.glob("*"):
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
                results.append({
                    "file": file.name,
                    "destination": str(safe_destination),
                    "status": "would_move"
                })
            else:
                try:
                    shutil.move(file, safe_destination)
                    results.append({
                        "file": file.name,
                        "destination": str(safe_destination),
                        "status": "moved"
                    })
                except Exception as e:
                    results.append({
                        "file": file.name,
                        "destination": None,
                        "status": "error",
                        "error": str(e)
                    })
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default=None, help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    args = parser.parse_args()

    if args.folder:
        results = organize_files(Path(args.folder), dry_run=args.dry_run)
    else:
        results = organize_files(Path.home() / "Downloads", dry_run=args.dry_run) + \
                    organize_files(Path.home() / "Desktop", dry_run=args.dry_run)

    for r in results:
        if r["status"] == "moved":
            logging.info(f"Moved: {r['file']} -> {r['destination']}")
        elif r["status"] == "would_move":
            logging.info(f"[DRY RUN] Would move: {r['file']} -> {r['destination']}")
        else:
            logging.error(f"Skipped {r['file']}: {r['error']}")
    logging.info("Done! Your folders are organized.")

if __name__ == "__main__":
    main()