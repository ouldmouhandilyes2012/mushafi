from __future__ import annotations

import json
from pathlib import Path


class TafsirService:
    def __init__(self, app_root: str | Path):
        self.app_root = Path(app_root)
        self.tafsir_root = self.app_root / "assets" / "tafsir"

    def list_available_tafsir(self):
        if not self.tafsir_root.exists():
            return []
        return [path.name for path in self.tafsir_root.iterdir() if path.is_file() and path.suffix.lower() == ".json"]

    def load_tafsir(self, file_name: str):
        path = self.tafsir_root / file_name
        if not path.exists():
            return {}
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            return data
        except (OSError, ValueError, json.JSONDecodeError):
            return {}

    def find_tafsir_for_ayah(self, surah: int, ayah: int, file_name: str = None):
        if not file_name:
            files = self.list_available_tafsir()
            if not files:
                return None
            file_name = files[0]

        data = self.load_tafsir(file_name)
        if not isinstance(data, list):
            return None

        for item in data:
            if item.get("surah_number") == surah and item.get("ayah_number") == ayah:
                return {
                    "text": item.get("tafsir", ""),
                    "source": item.get("source", ""),
                }
        return None
