from __future__ import annotations

import json
from pathlib import Path


class QuranDataImporter:
    """Loads verified local Quran JSON files into the app."""

    def __init__(self, app_root: str | Path):
        self.app_root = Path(app_root)

    def list_available_files(self):
        quran_root = self.app_root / "assets" / "quran"
        if not quran_root.exists():
            return []
        files = []
        for directory in quran_root.iterdir():
            if directory.is_dir():
                for f in directory.iterdir():
                    if f.suffix.lower() == ".json":
                        files.append(str(f))
        return files

    def import_file(self, file_path: str | Path):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"No such file: {path}")
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("Quran import files must contain a JSON array of verse objects.")
        return data
