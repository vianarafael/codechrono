import sqlite3
import os

DB_PATH = "data/sessions.db"
os.makedirs("data", exist_ok=True)


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            start_time INTEGER,
            end_time INTEGER,
            duration INTEGER,
            summary TEXT
        )
        """)
        conn.commit()



def create_session(message, start_ts):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sessions (message, start_time, end_time, summary) VALUES (?, ?, ?, ?)",
            (message, start_ts, None, None)
        )
        conn.commit()


def finalize_session(start_ts, end_ts, summary):
    duration = end_ts - start_ts
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE sessions
            SET end_time = ?, duration = ?, summary = ?
            WHERE start_time = ?
        """, (end_ts, duration, summary, start_ts))
        conn.commit()

def get_recent_summaries(limit=5):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT message, start_time as start, end_time as end, summary
            FROM sessions
            WHERE summary IS NOT NULL
            ORDER BY start_time DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cur.fetchall()]
    
def get_last_unfinished_session():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT start_time FROM sessions
            WHERE end_time IS NULL
            ORDER BY start_time DESC
            LIMIT 1
        """)
        row = cur.fetchone()
        return row[0] if row else None

def get_estimation_data():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT message, (end_time - start_time) as duration, summary
            FROM sessions
            WHERE summary IS NOT NULL AND end_time IS NOT NULL
        """)
        return [dict(row) for row in cur.fetchall()]


