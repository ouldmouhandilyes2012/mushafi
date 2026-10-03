from dataclasses import dataclass


@dataclass
class Riwayah:
    id: int = 0
    name: str = ""
    display_name: str = ""
    file_path: str = ""
    is_active: int = 0
