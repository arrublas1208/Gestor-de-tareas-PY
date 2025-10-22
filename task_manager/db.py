import sqlite3
from typing import Optional
from .config import DB_PATH

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL CHECK(status IN ('pending','in_progress','done')),
    priority TEXT NOT NULL CHECK(priority IN ('low','medium','high')),
    due_date TEXT,
    tags TEXT, -- JSON string (list of strings)
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def get_connection(path: Optional[str] = None) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path or DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: Optional[sqlite3.Connection] = None) -> None:
    owns_conn = False
    if conn is None:
        conn = get_connection()
        owns_conn = True
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        if owns_conn:
            conn.close()