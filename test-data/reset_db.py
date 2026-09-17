#!/usr/bin/env python3
"""Reset the application database to a known state: apply the schema, then seed.

Usage:  python3 test-data/reset_db.py
The database lives at application/insurance.db (gitignored — always regenerated).
All data below is synthetic; customers are deliberately named "Test <Greek letter>".
"""
import sqlite3
from pathlib import Path

from werkzeug.security import generate_password_hash

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "application" / "insurance.db"
SCHEMA = ROOT / "application" / "schema.sql"

USERS = [
    # username, plain password (synthetic, documented for the lab), role
    ("agent1", "Agent#Test1", "agent"),
    ("manager1", "Manager#Test1", "manager"),
]

CUSTOMERS = [
    # first, last, birth_date, email
    ("Test", "Alpha", "1980-05-14", "test.alpha@example.test"),
    ("Test", "Beta", "1961-09-30", "test.beta@example.test"),   # near the age-65 boundary
    ("Test", "Gamma", "1995-01-02", "test.gamma@example.test"),
]

POLICIES = [
    # number, customer_id, product, coverage, premium, status, start, end, created_by
    ("POL-2026-0001", 1, "LIFE_TERM", 100000, 42.50, "ACTIVE", "2026-01-01", "2036-01-01", 1),
    ("POL-2026-0002", 2, "LIFE_WHOLE", 250000, 180.00, "PENDING", "2026-09-01", "2046-09-01", 1),
    ("POL-2020-0003", 3, "LIFE_TERM", 50000, 21.00, "EXPIRED", "2020-01-01", "2025-01-01", 1),
]


def reset() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA.read_text())
        conn.executemany(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            [(u, generate_password_hash(p), r) for u, p, r in USERS],
        )
        conn.executemany(
            "INSERT INTO customers (first_name, last_name, birth_date, email) VALUES (?, ?, ?, ?)",
            CUSTOMERS,
        )
        conn.executemany(
            "INSERT INTO policies (policy_number, customer_id, product_type, coverage_amount,"
            " premium, status, start_date, end_date, created_by)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            POLICIES,
        )
        conn.commit()
    finally:
        conn.close()
    print(f"Database reset: {DB_PATH}")
    print(f"  users={len(USERS)} customers={len(CUSTOMERS)} policies={len(POLICIES)}")


if __name__ == "__main__":
    reset()
