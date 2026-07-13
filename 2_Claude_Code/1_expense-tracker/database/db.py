import sqlite3
from datetime import datetime
from pathlib import Path

from werkzeug.security import generate_password_hash

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "expense_tracker.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    try:
        existing = conn.execute("SELECT COUNT(*) AS cnt FROM users").fetchone()
        if existing["cnt"] > 0:
            return

        password_hash = generate_password_hash("demo123")
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cur.lastrowid

        year_month = datetime.now().strftime("%Y-%m")
        sample_expenses = [
            (user_id, 45.50, "Food", f"{year_month}-02", "Grocery shopping"),
            (user_id, 12.00, "Transport", f"{year_month}-03", "Bus fare"),
            (user_id, 89.99, "Bills", f"{year_month}-05", "Electricity bill"),
            (user_id, 25.00, "Health", f"{year_month}-07", "Pharmacy purchase"),
            (user_id, 15.75, "Entertainment", f"{year_month}-10", "Movie ticket"),
            (user_id, 60.20, "Shopping", f"{year_month}-14", "New shoes"),
            (user_id, 10.00, "Other", f"{year_month}-18", "Miscellaneous item"),
            (user_id, 22.30, "Food", f"{year_month}-21", "Restaurant dinner"),
        ]
        conn.executemany(
            """INSERT INTO expenses (user_id, amount, category, date, description)
               VALUES (?, ?, ?, ?, ?)""",
            sample_expenses,
        )
        conn.commit()
    finally:
        conn.close()
