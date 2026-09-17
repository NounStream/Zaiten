"""AG Insurance QA Lab — application under test.

Small Flask app, deliberately built for testability: every interactive
element carries a stable id (see templates/) so UI automation never
relies on brittle selectors.
"""
import os
import sqlite3
from functools import wraps
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

DB_PATH = Path(__file__).resolve().parent / "insurance.db"

app = Flask(__name__)
# Dev-only default; a real deployment must set SECRET_KEY in the environment.
app.secret_key = os.environ.get("SECRET_KEY", "qa-lab-dev-secret")


# --- database helpers -------------------------------------------------------

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# --- auth -------------------------------------------------------------------

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("dashboard") if "user_id" in session else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        row = get_db().execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if row and check_password_hash(row["password_hash"], password):
            session.clear()
            session["user_id"] = row["id"]
            session["username"] = row["username"]
            session["role"] = row["role"]
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    counts = get_db().execute(
        "SELECT status, COUNT(*) AS n FROM policies GROUP BY status"
    ).fetchall()
    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"],
        counts={row["status"]: row["n"] for row in counts},
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
