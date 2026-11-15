from datetime import date
from pathlib import Path
import shutil
import csv
import io
import math
import sqlite3
import os

from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__, instance_relative_config=True)
Path(app.instance_path).mkdir(parents=True, exist_ok=True)
DB_PATH = Path(app.instance_path) / "followup_pilot.db"
LEGACY_DB_PATH = Path(__file__).resolve().parent / "followup_pilot.db"
if LEGACY_DB_PATH.exists() and not DB_PATH.exists():
    shutil.copy2(LEGACY_DB_PATH, DB_PATH)
STATUSES = {"New", "Contacted", "Interested", "Converted", "Lost"}


def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT DEFAULT '',
            email TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            source TEXT DEFAULT 'Other',
            status TEXT DEFAULT 'New',
            value REAL DEFAULT 0,
            follow_up TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")


def clean(data, old=None):
    old = dict(old or {})
    item = {
        key: data.get(key, old.get(key, ""))
        for key in ("name", "company", "email", "phone", "source",
                    "status", "value", "follow_up", "notes")
    }
    item["name"] = str(item["name"]).strip()
    if not item["name"]:
        raise ValueError("Lead name is required.")
    if item["status"] not in STATUSES:
        raise ValueError("Choose a valid lead status.")
    try:
        value = float(item["value"] or 0)
    except (TypeError, ValueError):
        raise ValueError("Deal value must be a valid number.")
    if not math.isfinite(value) or value < 0:
        raise ValueError("Deal value must be zero or greater.")
    item["value"] = value
    for key in ("company", "email", "phone", "source", "follow_up", "notes"):
        item[key] = str(item[key] or "").strip()
    return item


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/leads")
def leads():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    due = request.args.get("due", "")
    sql, args = "SELECT * FROM leads WHERE 1=1", []
    if q:
        sql += " AND (name LIKE ? OR company LIKE ? OR email LIKE ? OR phone LIKE ?)"
        args += [f"%{q}%"] * 4
    if status in STATUSES:
        sql += " AND status=?"
        args.append(status)
    if due in ("upcoming", "overdue"):
        op = ">=" if due == "upcoming" else "<"
        sql += f" AND follow_up<>'' AND follow_up {op} ? AND status NOT IN ('Converted','Lost')"
        args.append(date.today().isoformat())
    sql += " ORDER BY CASE WHEN follow_up='' THEN 1 ELSE 0 END, follow_up, updated_at DESC"
    with connect() as db:
        return jsonify([dict(row) for row in db.execute(sql, args)])


@app.post("/api/leads")
def add_lead():
    try:
        item = clean(request.get_json(silent=True) or {})
    except (ValueError, TypeError):
        return jsonify(error="Check the lead name, status and deal value."), 400
    with connect() as db:
        cur = db.execute("""INSERT INTO leads
            (name, company, email, phone, source, status, value, follow_up, notes)
            VALUES (:name, :company, :email, :phone, :source, :status, :value, :follow_up, :notes)""", item)
        row = db.execute("SELECT * FROM leads WHERE id=?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201


@app.route("/api/leads/<int:lead_id>", methods=["GET", "PATCH", "DELETE"])
def lead(lead_id):
    with connect() as db:
        row = db.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
        if not row:
            return jsonify(error="Lead not found."), 404
        if request.method == "GET":
            return jsonify(dict(row))
        if request.method == "DELETE":
            db.execute("DELETE FROM leads WHERE id=?", (lead_id,))
            return jsonify(ok=True)
        try:
            item = clean(request.get_json(silent=True) or {}, row)
        except (ValueError, TypeError):
            return jsonify(error="Check the lead name, status and deal value."), 400
        db.execute("""UPDATE leads SET name=:name, company=:company, email=:email, phone=:phone,
            source=:source, status=:status, value=:value, follow_up=:follow_up, notes=:notes,
            updated_at=CURRENT_TIMESTAMP WHERE id=:id""", {**item, "id": lead_id})
        saved = db.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
        return jsonify(dict(saved))


@app.get("/api/stats")
def stats():
    today = date.today().isoformat()
    with connect() as db:
        total = db.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        converted = db.execute("SELECT COUNT(*) FROM leads WHERE status='Converted'").fetchone()[0]
        pipeline = db.execute("SELECT COALESCE(SUM(value),0) FROM leads WHERE status NOT IN ('Converted','Lost')").fetchone()[0]
        overdue = db.execute("SELECT COUNT(*) FROM leads WHERE follow_up<>'' AND follow_up<? AND status NOT IN ('Converted','Lost')", (today,)).fetchone()[0]
        due = db.execute("SELECT COUNT(*) FROM leads WHERE follow_up=? AND status NOT IN ('Converted','Lost')", (today,)).fetchone()[0]
        stages = db.execute("SELECT status, COUNT(*) n FROM leads GROUP BY status").fetchall()
    return jsonify(total=total, converted=converted, pipeline=pipeline, overdue=overdue,
                   due_today=due, conversion_rate=round(converted * 100 / total) if total else 0,
                   stages={row["status"]: row["n"] for row in stages})


@app.get("/api/export")
def export():
    with connect() as db:
        rows = db.execute("""SELECT name, company, email, phone, source, status,
            value, follow_up, notes, created_at FROM leads""").fetchall()
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["Name", "Company", "Email", "Phone", "Source", "Status",
                     "Deal value", "Follow-up", "Notes", "Created"])
    writer.writerows([tuple(row) for row in rows])
    response = make_response("\ufeff" + out.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=followup-pilot-leads.csv"
    return response


@app.get("/api/health")
def health():
    try:
        with connect() as db:
            db.execute("SELECT 1")
        return jsonify(status="ok", database="connected")
    except sqlite3.Error:
        app.logger.exception("Database health check failed")
        return jsonify(status="error", database="unavailable"), 503


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return jsonify(error="The requested API endpoint was not found."), 404
    return error


@app.errorhandler(500)
def internal_error(error):
    app.logger.exception("Unexpected application error")
    if request.path.startswith("/api/"):
        return jsonify(error="Something went wrong. Please try again."), 500
    return "Something went wrong. Please restart the app and try again.", 500


init_db()

if __name__ == "__main__":
    # Local-only development server. Use a production WSGI server for deployment.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
