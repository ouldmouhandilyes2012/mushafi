from __future__ import annotations

from datetime import datetime, timedelta
import sqlite3


class ReviewEngine:
    def __init__(self):
        pass

    def add_review(self, connection: sqlite3.Connection, surah: int, ayah_start: int, ayah_end: int, success: bool, mistakes: int = 0):
        interval = 7 if success else 2
        connection.execute(
            """
            INSERT INTO reviews (surah, ayah_start, ayah_end, due_date, interval_days, mistakes, success_count, last_review, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')
            """,
            (surah, ayah_start, ayah_end, (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d"), interval, mistakes, 1 if success else 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        connection.commit()

    def list_due_reviews(self, connection: sqlite3.Connection):
        return connection.execute("SELECT * FROM reviews WHERE status != 'done' ORDER BY due_date ASC").fetchall()

    def get_dashboard(self, connection: sqlite3.Connection):
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "today": connection.execute("SELECT COUNT(*) FROM reviews WHERE due_date <= ? AND status != 'done'", (today,)).fetchone()[0],
            "upcoming": connection.execute("SELECT COUNT(*) FROM reviews WHERE due_date > ? AND status != 'done'", (today,)).fetchone()[0],
            "late": connection.execute("SELECT COUNT(*) FROM reviews WHERE due_date < ? AND status != 'done'", (today,)).fetchone()[0],
        }
