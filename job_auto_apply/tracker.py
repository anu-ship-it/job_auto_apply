"""
Local SQLite tracker. Two jobs it does:
1. Prevents double-applying to the same job_id.
2. Gives you a queryable log of everything you've applied to, and when.

This is not optional infrastructure - without it you WILL apply twice to
the same job or lose track of what you sent where.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def init_db(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            job_id TEXT,
            source TEXT,
            company TEXT,
            title TEXT,
            url TEXT,
            score REAL,
            status TEXT,          -- applied | failed | skipped
            applied_at TEXT,
            PRIMARY KEY (job_id, source)
        )
    """)
    conn.commit()
    conn.close()


def already_applied(db_path: Path, job_id: str, source: str) -> bool:
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        "SELECT 1 FROM applications WHERE job_id = ? AND source = ?",
        (job_id, source),
    ).fetchone()
    conn.close()
    return row is not None


def log_application(db_path: Path, job: dict, status: str) -> None:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """INSERT OR REPLACE INTO applications
           (job_id, source, company, title, url, score, status, applied_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            job["job_id"], job["source"], job["company"], job["title"],
            job["url"], job.get("score", 0), status,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()
