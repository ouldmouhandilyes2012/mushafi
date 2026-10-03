from dataclasses import dataclass


@dataclass
class Review:
    id: int = 0
    surah: int = 0
    ayah_start: int = 0
    ayah_end: int = 0
    due_date: str = ""
    interval_days: int = 1
    mistakes: int = 0
    success_count: int = 0
    last_review: str = ""
    status: str = "pending"
