from dataclasses import dataclass


@dataclass
class Reader:
    id: int = 0
    reader_id: str = ""
    name: str = ""
    riwayah: str = ""
    audio_path: str = ""
    is_active: int = 0
