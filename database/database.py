import sqlite3
from pathlib import Path

from database.migrations import run_migrations


DEFAULT_DB_PATH = Path(__file__).resolve().parent / "mushafi.db"


class Database:
    def __init__(self, db_path: str | Path | None = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
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


def get_db() -> Database:
    return Database()
