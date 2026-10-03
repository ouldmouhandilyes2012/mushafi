from dataclasses import dataclass


@dataclass
class Surah:
    id: int = 0
    surah_number: int = 0
    name_ar: str = ""
    name_en: str = ""
    revelation_place: str = ""
    verses_count: int = 0
