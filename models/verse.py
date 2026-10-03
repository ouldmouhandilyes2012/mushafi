from dataclasses import dataclass


@dataclass
class Verse:
    id: int = 0
    surah_number: int = 0
    ayah_number: int = 0
    text: str = ""
    text_english: str = ""
    translation: str = ""
