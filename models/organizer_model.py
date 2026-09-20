"""Model layer: file scanning, organization, duplicate detection, logging, and undo."""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

APP_DIR = Path.home() / ".smart_file_organizer"
LOG_FILE = APP_DIR / "organizer.log"
HISTORY_FILE = APP_DIR / "last_operation.json"

CATEGORY_MAP = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".java", ".c", ".cpp", ".php", ".sql"},
}


@dataclass
class MoveRecord:
    source: str
    destination: str


class FileOrganizerModel:
    def __init__(self) -> None:
        APP_DIR.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
        )

    @staticmethod
    def category_for(file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        for category, extensions in CATEGORY_MAP.items():
            if suffix in extensions:
                return category
        return "Others"

    @staticmethod
    def unique_destination(destination: Path) -> Path:
        if not destination.exists():
            return destination
        counter = 1
        while True:
            candidate = destination.with_name(f"{destination.stem} ({counter}){destination.suffix}")
            if not candidate.exists():
                return candidate
            counter += 1

    @staticmethod
    def file_hash(file_path: Path, chunk_size: int = 1024 * 1024) -> str:
        digest = hashlib.sha256()
        with file_path.open("rb") as file:
            for chunk in iter(lambda: file.read(chunk_size), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def scan(self, directory: Path, organize_by_date: bool = False) -> list[dict]:
        if not directory.is_dir():
            raise ValueError("Please select a valid folder.")

        results: list[dict] = []
        for item in sorted(directory.iterdir(), key=lambda path: path.name.lower()):
            if not item.is_file():
                continue
            category = self.category_for(item)
            target_folder = directory / category
            if organize_by_date:
                month = datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m")
                target_folder = target_folder / month
            results.append({
                "name": item.name,
                "path": str(item),
                "category": category,
                "target": str(target_folder / item.name),
                "size": item.stat().st_size,
            })
        return results

    def organize(self, directory: Path, organize_by_date: bool, progress: Callable[[str], None] | None = None) -> list[MoveRecord]:
        records: list[MoveRecord] = []
        for row in self.scan(directory, organize_by_date):
            source = Path(row["path"])
            target = self.unique_destination(Path(row["target"]))
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target))
            records.append(MoveRecord(source=str(source), destination=str(target)))
            logging.info("Moved: %s -> %s", source, target)
            if progress:
                progress(f"Moved: {source.name} → {target.parent.name}")

        HISTORY_FILE.write_text(
            json.dumps({
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "moves": [asdict(record) for record in records],
            }, indent=2),
            encoding="utf-8",
        )
        return records

    def find_duplicates(self, directory: Path) -> list[list[Path]]:
        grouped: dict[str, list[Path]] = defaultdict(list)
        for item in directory.iterdir():
            if item.is_file():
                try:
                    grouped[self.file_hash(item)].append(item)
                except OSError as error:
                    logging.warning("Could not hash %s: %s", item, error)
        return [files for files in grouped.values() if len(files) > 1]

    def undo_last_operation(self, progress: Callable[[str], None] | None = None) -> tuple[int, list[str]]:
        if not HISTORY_FILE.exists():
            raise FileNotFoundError("No previous operation is available to undo.")

        history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        restored = 0
        errors: list[str] = []
        for record in reversed(history.get("moves", [])):
            source = Path(record["source"])
            destination = Path(record["destination"])
            try:
                if not destination.exists():
                    errors.append(f"Missing file: {destination.name}")
                    continue
                source.parent.mkdir(parents=True, exist_ok=True)
                restore_path = self.unique_destination(source)
                shutil.move(str(destination), str(restore_path))
                restored += 1
                logging.info("Restored: %s -> %s", destination, restore_path)
                if progress:
                    progress(f"Restored: {restore_path.name}")
            except OSError as error:
                errors.append(f"{destination.name}: {error}")

        if not errors:
            HISTORY_FILE.unlink(missing_ok=True)
        return restored, errors
