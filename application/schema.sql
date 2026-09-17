-- Schema for the AG Insurance QA Lab application under test.
-- Applied by test-data/reset_db.py; the database file itself is never committed.

DROP TABLE IF EXISTS policies;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL CHECK (role IN ('agent', 'manager'))
);

CREATE TABLE customers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name  TEXT    NOT NULL,
    last_name   TEXT    NOT NULL,
    birth_date  TEXT    NOT NULL,              -- ISO 8601 (YYYY-MM-DD)
    email       TEXT    NOT NULL UNIQUE
);

CREATE TABLE policies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_number   TEXT    NOT NULL UNIQUE,   -- e.g. POL-2026-0001
    customer_id     INTEGER NOT NULL REFERENCES customers (id),
    product_type    TEXT    NOT NULL CHECK (product_type IN ('LIFE_TERM', 'LIFE_WHOLE')),
    coverage_amount REAL    NOT NULL,
    premium         REAL    NOT NULL,
    status          TEXT    NOT NULL CHECK (status IN ('PENDING', 'ACTIVE', 'EXPIRED', 'CANCELLED')),
    start_date      TEXT    NOT NULL,
    end_date        TEXT    NOT NULL,
    created_by      INTEGER NOT NULL REFERENCES users (id)
);
