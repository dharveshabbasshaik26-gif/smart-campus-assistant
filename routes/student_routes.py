from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
from models.db import get_db

student_bp = Blueprint("student", __name__)


# STUDENT LOGIN
@student_bp.route("/student_login", methods=["GET","POST"])
def student_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        student = conn.execute(
            "SELECT * FROM students WHERE username=?",
            (username,)
        ).fetchone()

        if student and check_password_hash(student["password_hash"], password):

            session["student"] = student["id"]

            return redirect("/student_dashboard")

    return render_template("student_login.html")


# STUDENT DASHBOARD
@student_bp.route("/student_dashboard")
def student_dashboard():

    if not session.get("student"):
        return redirect("/student_login")

    return render_template("student_dashboard.html")