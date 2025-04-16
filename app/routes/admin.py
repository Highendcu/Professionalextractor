from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app.models.user import load_users, save_users
from datetime import datetime, timedelta
from functools import wraps
import json
import os
import uuid
import random
import string
from app.services.validator import validate_credentials

admin = Blueprint("admin", __name__, template_folder="../templates")

USER_DB_PATH = os.path.join("app", "data", "users.json")
DEFAULT_ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
DEFAULT_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "12345")

def load_users():
    if not os.path.exists(USER_DB_PATH):
        return []
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f, indent=2)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin_logged_in" not in session:
            return redirect(url_for("admin.admin_login"))
        return f(*args, **kwargs)
    return decorated

@admin.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    username_env = os.getenv("ADMIN_USERNAME", DEFAULT_ADMIN_USERNAME)
    password_env = os.getenv("ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username == username_env and password == password_env:
            session["admin_logged_in"] = True
            return redirect(url_for("admin.admin_dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@admin.route("/logout")
@login_required
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("main.index"))

@admin.route("/admin-dashboard")
@login_required
def admin_dashboard():
    users = load_users()
    page = int(request.args.get("page", 1))
    per_page = 10
    total_pages = (len(users) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    for user in users:
        expiry = user.get("expiry")
        try:
            user["expiry_dt"] = datetime.fromisoformat(expiry) if expiry else None
        except Exception:
            user["expiry_dt"] = None

    return render_template("admin.html",
                           users=users[start:end],
                           page=page,
                           total_pages=total_pages,
                           now=datetime.utcnow())

@admin.route("/generate-user", methods=["POST"])
@login_required
def generate_user():
    username = f"user-{uuid.uuid4().hex[:6]}"
    password = uuid.uuid4().hex[:8]
    expiry = (datetime.utcnow() + timedelta(weeks=1)).isoformat()

    users = load_users()
    users.append({
        "username": username,
        "password": password,
        "created_at": datetime.utcnow().isoformat(),
        "expiry": expiry
    })
    save_users(users)
    return jsonify({"username": username, "password": password, "expiry": expiry})

@admin.route("/revoke-user/<username>", methods=["POST"])
@login_required
def revoke_user(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            user["expiry"] = datetime.utcnow().isoformat()
    save_users(users)
    return redirect(url_for("admin.admin_dashboard"))

@admin.route("/edit-user/<username>")
@login_required
def edit_user_form(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return render_template("edit_user.html", user=user)
    return redirect(url_for("admin.admin_dashboard"))

@admin.route("/edit-user/<username>", methods=["POST"])
@login_required
def update_user(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            user["password"] = request.form.get("password", user["password"])
            user["expiry"] = request.form.get("expiry", user["expiry"])
    save_users(users)
    return redirect(url_for("admin.admin_dashboard"))

@admin.route("/export-csv")
@login_required
def export_csv():
    import csv
    from io import StringIO
    users = load_users()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Username", "Password", "Expiry", "Revoked"])
    for user in users:
        writer.writerow([user["username"], user["password"], user["expiry"], user.get("revoked", False)])
    output.seek(0)
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="users.csv"
    )

@admin.route('/verify-credentials', methods=['POST'])
def verify_credentials():
    data = request.form or request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    valid, message = validate_credentials(username, password)
    if valid:
        session['license_valid'] = True
        return jsonify({"valid": True})
    return jsonify({"valid": False, "message": message})