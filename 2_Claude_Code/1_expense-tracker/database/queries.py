from datetime import datetime

from database.db import get_db


def get_user_by_id(user_id):
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        return None

    member_since = datetime.strptime(
        row["created_at"], "%Y-%m-%d %H:%M:%S"
    ).strftime("%B %Y")

    return {
        "name": row["name"],
        "email": row["email"],
        "member_since": member_since,
    }


def get_summary_stats(user_id):
    """Return {total_spent, transaction_count, top_category} for user_id.

    No expenses -> {"total_spent": 0, "transaction_count": 0, "top_category": "—"}.
    """
    conn = get_db()
    try:
        totals_row = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS cnt "
            "FROM expenses WHERE user_id = ?",
            (user_id,),
        ).fetchone()

        top_row = conn.execute(
            "SELECT category, SUM(amount) AS category_total "
            "FROM expenses WHERE user_id = ? "
            "GROUP BY category "
            "ORDER BY category_total DESC, category ASC "
            "LIMIT 1",
            (user_id,),
        ).fetchone()
    finally:
        conn.close()

    if totals_row["cnt"] == 0:
        return {"total_spent": 0, "transaction_count": 0, "top_category": "—"}

    return {
        "total_spent": totals_row["total"],
        "transaction_count": totals_row["cnt"],
        "top_category": top_row["category"],
    }


def get_recent_transactions(user_id, limit=10):
    """Return list of {date, description, category, amount}, newest-first.

    No expenses -> [].
    """
    conn = get_db()
    try:
        rows = conn.execute(
            """SELECT date, description, category, amount
               FROM expenses
               WHERE user_id = ?
               ORDER BY date DESC, id DESC
               LIMIT ?""",
            (user_id, limit),
        ).fetchall()
    finally:
        conn.close()

    return [
        {
            "date": row["date"],
            "description": row["description"],
            "category": row["category"],
            "amount": row["amount"],
        }
        for row in rows
    ]


def get_category_breakdown(user_id):
    """Return list of {name, amount, pct}, ordered by amount desc.

    pct values are integers summing to exactly 100 (largest category absorbs
    the rounding remainder). No expenses -> [].
    """
    conn = get_db()
    try:
        rows = conn.execute(
            """SELECT category, SUM(amount) as total
               FROM expenses
               WHERE user_id = ?
               GROUP BY category
               ORDER BY total DESC""",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        return []

    total_spend = sum(row["total"] for row in rows)

    breakdown = [
        {"name": row["category"], "amount": row["total"], "pct": 0}
        for row in rows
    ]

    raw_pcts = [
        (item["amount"] / total_spend) * 100 if total_spend else 0
        for item in breakdown
    ]
    rounded_pcts = [round(p) for p in raw_pcts]

    remainder = 100 - sum(rounded_pcts)
    rounded_pcts[0] += remainder

    for item, pct in zip(breakdown, rounded_pcts):
        item["pct"] = pct

    return breakdown
