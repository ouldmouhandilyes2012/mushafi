from __future__ import annotations

from pathlib import Path


def ensure_directories():
    base = Path(__file__).resolve().parent.parent
    dirs = [
        base / "assets" / "quran" / "hafs",
        base / "assets" / "quran" / "warsh",
        base / "assets" / "quran" / "qalun",
        base / "assets" / "audio",
        base / "assets" / "tafsir",
        base / "assets" / "fonts",
        base / "database",
        base / "models",
        base / "screens",
        base / "services",
        base / "widgets",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


ensure_directories()
