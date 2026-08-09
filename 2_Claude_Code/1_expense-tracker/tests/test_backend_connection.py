import itertools

import pytest

from app import app as flask_app
from database.db import get_db, init_db, seed_db
from database.queries import (
    get_category_breakdown,
    get_recent_transactions,
    get_summary_stats,
    get_user_by_id,
)

_empty_user_counter = itertools.count(1)


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setattr("database.db.DB_PATH", tmp_path / "test.db")
    flask_app.config.update(TESTING=True)
    with flask_app.app_context():
        init_db()
        seed_db()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def seed_user_id(app):
    with app.app_context():
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
            ).fetchone()
        finally:
            conn.close()
        return row["id"]


@pytest.fixture
def empty_user_id(app):
    email = f"noexpenses{next(_empty_user_counter)}@spendly.com"
    with app.app_context():
        conn = get_db()
        try:
            cur = conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                ("No Expenses", email, "hash"),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()


# ------------------------------------------------------------------ #
# get_user_by_id                                                      #
# ------------------------------------------------------------------ #

def test_get_user_by_id_valid(app, seed_user_id):
    with app.app_context():
        user = get_user_by_id(seed_user_id)
    assert user["name"] == "Demo User"
    assert user["email"] == "demo@spendly.com"
    assert user["member_since"]


def test_get_user_by_id_missing(app):
    with app.app_context():
        assert get_user_by_id(999999) is None


# Subagent 1: get_summary_stats tests go below this line

def test_get_summary_stats_with_expenses(app, seed_user_id):
    with app.app_context():
        stats = get_summary_stats(seed_user_id)
    assert stats["total_spent"] == pytest.approx(280.74)
    assert stats["transaction_count"] == 8
    assert stats["top_category"] == "Bills"


def test_get_summary_stats_no_expenses(app, empty_user_id):
    with app.app_context():
        stats = get_summary_stats(empty_user_id)
    assert stats == {"total_spent": 0, "transaction_count": 0, "top_category": "—"}


# Subagent 2: get_recent_transactions tests go below this line

def test_get_recent_transactions_seed_user(app, seed_user_id):
    with app.app_context():
        result = get_recent_transactions(seed_user_id)

    assert len(result) == 8
    for item in result:
        assert set(item.keys()) == {"date", "description", "category", "amount"}

    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_get_recent_transactions_empty_user(app, empty_user_id):
    with app.app_context():
        result = get_recent_transactions(empty_user_id)
    assert result == []


def test_get_recent_transactions_respects_limit(app, seed_user_id):
    with app.app_context():
        result = get_recent_transactions(seed_user_id, limit=3)
    assert len(result) == 3


# Subagent 3: get_category_breakdown tests go below this line

def test_get_category_breakdown_seed_user(app, seed_user_id):
    with app.app_context():
        result = get_category_breakdown(seed_user_id)

    assert len(result) == 7

    amounts = [item["amount"] for item in result]
    assert amounts == sorted(amounts, reverse=True)

    assert sum(item["pct"] for item in result) == 100


def test_get_category_breakdown_empty_user(app, empty_user_id):
    with app.app_context():
        result = get_category_breakdown(empty_user_id)
    assert result == []


# ------------------------------------------------------------------ #
# GET /profile route                                                  #
# ------------------------------------------------------------------ #

def test_profile_unauthenticated_redirects_to_login(client):
    response = client.get("/profile")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_profile_authenticated_seed_user(client, seed_user_id):
    with client.session_transaction() as sess:
        sess["user_id"] = seed_user_id

    response = client.get("/profile")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Demo User" in body
    assert "demo@spendly.com" in body
    assert "₹" in body
    assert "280.74" in body
    assert "Bills" in body

    with client.application.app_context():
        stats = get_summary_stats(seed_user_id)
    assert stats["transaction_count"] == 8
