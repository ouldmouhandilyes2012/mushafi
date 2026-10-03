import sqlite3
from pathlib import Path

from database.migrations import run_migrations


DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "mushafi.db"


class Database:
    def __init__(self, db_path: str | Path | None = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")
        run_migrations(self.connection)

    def execute(self, query: str, params=()):
        cursor = self.connection.execute(query, params)
        self.connection.commit()
        return cursor

    def fetch_all(self, query: str, params=()):
        return self.connection.execute(query, params).fetchall()

    def fetch_one(self, query: str, params=()):
        return self.connection.execute(query, params).fetchone()

    def close(self):
        self.connection.close()

    def set_setting(self, key: str, value: str):
        self.execute(
            "INSERT INTO settings(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP",
            (key, value),
        )
        return value

    def get_setting(self, key: str, default: str = "") -> str:
        row = self.fetch_one("SELECT value FROM settings WHERE key = ?", (key,))
        return row["value"] if row else default

    def update_profile(self, **kwargs):
        current = self.get_profile()
        data = {
            "display_name": kwargs.get("display_name", current.get("display_name", "المستخدم")),
            "favorite_riwayah": kwargs.get("favorite_riwayah", current.get("favorite_riwayah", "hafs")),
            "favorite_reader": kwargs.get("favorite_reader", current.get("favorite_reader", "")),
            "memorization_goal": kwargs.get("memorization_goal", current.get("memorization_goal", 30)),
            "review_goal": kwargs.get("review_goal", current.get("review_goal", 10)),
        }
        self.execute(
            """
            UPDATE profile
            SET display_name = ?, favorite_riwayah = ?, favorite_reader = ?, memorization_goal = ?, review_goal = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
            """,
            (
                data["display_name"],
                data["favorite_riwayah"],
                data["favorite_reader"],
                data["memorization_goal"],
                data["review_goal"],
            ),
        )
        return data

    def get_profile(self) -> dict:
        row = self.fetch_one("SELECT * FROM profile WHERE id = 1")
        if not row:
            return {
                "display_name": "المستخدم",
                "favorite_riwayah": "hafs",
                "favorite_reader": "",
                "memorization_goal": 30,
                "review_goal": 10,
            }
        return {
            "display_name": row["display_name"],
            "favorite_riwayah": row["favorite_riwayah"],
            "favorite_reader": row["favorite_reader"],
            "memorization_goal": row["memorization_goal"],
            "review_goal": row["review_goal"],
        }

    def update_surah_status(self, surah_number: int, status: str):
        self.execute(
            """
            INSERT INTO surah_progress(surah_number, status, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(surah_number)
            DO UPDATE SET status = excluded.status, updated_at = CURRENT_TIMESTAMP
            """,
            (surah_number, status),
        )
        return status

    def get_surah_statuses(self) -> dict:
        rows = self.fetch_all("SELECT surah_number, status FROM surah_progress")
        return {row["surah_number"]: row["status"] for row in rows}

    def get_statistics_summary(self) -> dict:
        total_memorized = self.fetch_one("SELECT COUNT(*) FROM surah_progress WHERE status = 'memorized'")[0]
        total_review = self.fetch_one("SELECT COUNT(*) FROM surah_progress WHERE status = 'review'")[0]
        total_unmemorized = self.fetch_one("SELECT COUNT(*) FROM surah_progress WHERE status = 'unmemorized'")[0]
        return {
            "memorized": total_memorized,
            "review": total_review,
            "unmemorized": total_unmemorized,
        }


def get_db() -> Database:
    return Database()
