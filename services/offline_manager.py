from __future__ import annotations

from pathlib import Path


class OfflineManager:
    def __init__(self, app_root: str | Path):
        self.app_root = Path(app_root)

    def list_riwayat(self):
        quran_dir = self.app_root / "assets" / "quran"
        if not quran_dir.exists():
            return []
        return [path.name for path in quran_dir.iterdir() if path.is_dir()]

    def list_tafsir(self):
        tafsir_dir = self.app_root / "assets" / "tafsir"
        if not tafsir_dir.exists():
            return []
        return [path.name for path in tafsir_dir.iterdir() if path.is_file()]

    def list_readers(self):
        audio_dir = self.app_root / "assets" / "audio"
        if not audio_dir.exists():
            return []
        return [path.name for path in audio_dir.iterdir() if path.is_dir()]

    def get_content_summary(self):
        return {
            "riwayat": self.list_riwayat(),
            "tafsir": self.list_tafsir(),
            "readers": self.list_readers(),
        }
