from __future__ import annotations

from datetime import datetime, timedelta
import sqlite3


class ReviewEngine:
    def __init__(self):
        pass

    def add_review(self, connection: sqlite3.Connection, surah: int, ayah_start: int, ayah_end: int, success: bool, mistakes: int = 0):
        interval = 7 if success else 2
        due_date = (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d")

        connection.execute(
            """
            INSERT INTO reviews (surah, ayah_start, ayah_end, due_date, interval_days, mistakes, success_count, last_review, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')
            """,
            (surah, ayah_start, ayah_end, due_date, interval, mistakes, 1 if success else 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        connection.commit()

    def list_due_reviews(self, connection: sqlite3.Connection):
        return connection.execute("SELECT * FROM reviews WHERE status != 'done' ORDER BY due_date ASC").fetchall()

    def mark_review_done(self, connection: sqlite3.Connection, review_id: int):
        connection.execute(
            "UPDATE reviews SET status = 'done' WHERE id = ?",
            (review_id,),
        )
        connection.commit()

    def get_dashboard(self, connection: sqlite3.Connection):
        today = datetime.now().strftime("%Y-%m-%d")
        due_today = connection.execute(
            "SELECT COUNT(*) FROM reviews WHERE due_date = ? AND status != 'done'",
            (today,),
        ).fetchone()[0]
        upcoming = connection.execute(
            "SELECT COUNT(*) FROM reviews WHERE due_date > ? AND status != 'done'",
            (today,),
        ).fetchone()[0]
        overdue = connection.execute(
            "SELECT COUNT(*) FROM reviews WHERE due_date < ? AND status != 'done'",
            (today,),
        ).fetchone()[0]
        return {
            "today": due_today,
            "upcoming": upcoming,
            "overdue": overdue,
        }

    def update_review_interval(self, connection: sqlite3.Connection, review_id: int, success: bool, mistakes: int = 0):
        review = connection.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()
        if not review:
            return False

        current_interval = review["interval_days"]
        if success:
            new_interval = min(30, current_interval + 3)
        else:
            new_interval = max(1, current_interval - 1)

        due_date = (datetime.now() + timedelta(days=new_interval)).strftime("%Y-%m-%d")
        new_success_count = review["success_count"] + (1 if success else 0)
        new_mistakes = review["mistakes"] + mistakes

        connection.execute(
            """
            UPDATE reviews
            SET interval_days = ?, due_date = ?, success_count = ?, mistakes = ?, last_review = ?
            WHERE id = ?
            """,
            (new_interval, due_date, new_success_count, new_mistakes, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), review_id),
        )
        connection.commit()
        return True
