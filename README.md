# File Organizer Automation 🗂️

A Python automation script that automatically sorts your Downloads and Desktop folders by file type and date.

## What It Does
- Scans Downloads and Desktop folders
- Sorts files into folders by type (Images, Documents, Videos, Music)
- Organizes by date created (Year-Month)
- Creates destination folders automatically if they don't exist
- Skips open files gracefully without crashing

## How to Run
python file_organizer_automation.py                          # organizes real Downloads/Desktop
python file_organizer_automation.py --folder "path/to/folder" # organizes a specific folder

## Modules Used
- `pathlib` — building and finding folder paths, checking for filename collisions
- `shutil` — moving files
- `datetime` — organizing files by modification date
- `argparse` — CLI configuration (--folder flag for safe testing or scoped runs)

## Status

🚧 In active development — not yet ready for production use.

Done:
- Collision-safe file moving (no silent overwrites)
- No unnecessary re-processing of the tool's own output folders
- CLI configuration via --folder (safe scoped testing or real runs)
- Dry-run mode
- Structured logging instead of print statements
- Type hints and docstrings on all functions
- Test coverage (pytest) — 4 tests passing

Next up:
- Streamlit UI