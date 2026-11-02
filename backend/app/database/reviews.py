"""SQLite persistence for review history on the default branch."""

import json
import sqlite3
from pathlib import Path
from typing import Any

_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "reviews.sqlite3"


def _connect() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(_DB_PATH, timeout=5)
    connection.execute("CREATE TABLE IF NOT EXISTS reviews (review_id TEXT PRIMARY KEY, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, payload TEXT NOT NULL)")
    return connection


def save_review(review: dict[str, Any]) -> None:
    with _connect() as connection:
        connection.execute("INSERT OR REPLACE INTO reviews(review_id, payload) VALUES (?, ?)", (review["review_id"], json.dumps(review, ensure_ascii=False)))


def get_review(review_id: str) -> dict[str, Any] | None:
    with _connect() as connection:
        row = connection.execute("SELECT payload FROM reviews WHERE review_id = ?", (review_id,)).fetchone()
    return json.loads(row[0]) if row else None


def list_reviews(limit: int = 50) -> list[dict[str, Any]]:
    bounded_limit = max(1, min(limit, 100))
    with _connect() as connection:
        rows = connection.execute("SELECT payload FROM reviews ORDER BY created_at DESC, rowid DESC LIMIT ?", (bounded_limit,)).fetchall()
    return [json.loads(row[0]) for row in rows]
