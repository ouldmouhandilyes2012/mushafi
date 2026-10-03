from __future__ import annotations

from pathlib import Path

from kivy.core.audio import SoundLoader


class AudioService:
    def __init__(self, asset_root: str | Path | None = None):
        self.asset_root = Path(asset_root) if asset_root else Path(__file__).resolve().parent.parent / "assets"

    def list_audio_files(self):
        audio_dir = self.asset_root / "audio"
        if not audio_dir.exists():
            return []
        return [str(path) for path in audio_dir.rglob("*.*") if path.is_file()]

    def get_reader_audio(self, file_name: str):
        candidate = self.asset_root / "audio" / file_name
        if candidate.exists():
            return str(candidate)
        return ""

    def play_local_audio(self, file_name: str):
        path = self.get_reader_audio(file_name)
        if not path:
            return False
        sound = SoundLoader.load(path)
        if sound is not None:
            sound.play()
            return True
        return False
