import sqlite3


SCHEMA_SQL = [
    """
    CREATE TABLE IF NOT EXISTS app_meta (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS surahs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah_number INTEGER UNIQUE NOT NULL,
        name_ar TEXT NOT NULL,
        name_en TEXT,
        revelation_place TEXT,
        verses_count INTEGER DEFAULT 0
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah_number INTEGER NOT NULL,
        ayah_number INTEGER NOT NULL,
        text TEXT NOT NULL,
        text_english TEXT,
        translation TEXT,
        UNIQUE(surah_number, ayah_number)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS riwayat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        display_name TEXT NOT NULL,
        file_path TEXT,
        is_active INTEGER DEFAULT 0
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS readers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reader_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        riwayah TEXT,
        audio_path TEXT,
        is_active INTEGER DEFAULT 0
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS surah_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah_number INTEGER NOT NULL,
        status TEXT DEFAULT 'unmemorized',
        memorized INTEGER DEFAULT 0,
        needs_review INTEGER DEFAULT 0,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(surah_number)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS verse_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah_number INTEGER NOT NULL,
        ayah_number INTEGER NOT NULL,
        status TEXT DEFAULT 'unmemorized',
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(surah_number, ayah_number)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah INTEGER NOT NULL,
        ayah_start INTEGER NOT NULL,
        ayah_end INTEGER NOT NULL,
        due_date TEXT,
        interval_days INTEGER DEFAULT 1,
        mistakes INTEGER DEFAULT 0,
        success_count INTEGER DEFAULT 0,
        last_review TEXT,
        status TEXT DEFAULT 'pending'
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah_number INTEGER NOT NULL,
        ayah_number INTEGER NOT NULL,
        label TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_type TEXT NOT NULL,
        surah_number INTEGER,
        ayah_number INTEGER,
        note TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS recitations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah_number INTEGER NOT NULL,
        ayah_start INTEGER NOT NULL,
        ayah_end INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        notes TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS recordings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        duration_seconds REAL DEFAULT 0,
        is_personal INTEGER DEFAULT 1
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        value TEXT NOT NULL,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS statistics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        value TEXT NOT NULL,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        display_name TEXT,
        favorite_riwayah TEXT,
        favorite_reader TEXT,
        memorization_goal INTEGER DEFAULT 0,
        review_goal INTEGER DEFAULT 0,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """
]


def run_migrations(connection: sqlite3.Connection):
    for statement in SCHEMA_SQL:
        connection.execute(statement)

    defaults = {
        "font_size": "22",
        "night_mode": "0",
        "local_notifications": "1",
        "selected_riwayah": "hafs",
        "selected_reader": "",
    }
    for key, value in defaults.items():
        connection.execute(
            "INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)",
            (key, value),
        )

    if connection.execute("SELECT COUNT(*) FROM profile").fetchone()[0] == 0:
        connection.execute(
            "INSERT INTO profile(display_name, favorite_riwayah, favorite_reader, memorization_goal, review_goal) VALUES (?, ?, ?, ?, ?)",
            ("المستخدم", "hafs", "", 30, 10),
        )

    connection.commit()
