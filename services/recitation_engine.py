from __future__ import annotations

from datetime import datetime, timedelta


class RecitationEngine:
    def __init__(self):
        self.default_interval = 7

    def compute_next_interval(self, success_count: int, previous_interval: int = 0) -> int:
        if success_count <= 0:
            return max(1, previous_interval)
        return max(1, previous_interval + (success_count * 3))

    def schedule_review(self, surah_number: int, ayah_start: int, ayah_end: int, success: bool, mistakes: int = 0, previous_interval: int = 0):
        interval = self.compute_next_interval(1 if success else 0, previous_interval)
        if not success:
            interval = max(1, min(interval, 3))
        due_date = (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d")
        return {
            "surah": surah_number,
            "ayah_start": ayah_start,
            "ayah_end": ayah_end,
            "due_date": due_date,
            "interval_days": interval,
            "mistakes": mistakes,
            "success": success,
        }
