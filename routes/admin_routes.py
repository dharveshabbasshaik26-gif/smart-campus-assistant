from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from models.db import get_db

admin_bp = Blueprint("admin", __name__)


# ---------------- ADMIN LOGIN ----------------
@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        if user and check_password_hash(user["password_hash"], password):

            session["admin"] = True
            return redirect("/dashboard")

        return "Invalid Login"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@admin_bp.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    total_courses = conn.execute(
        "SELECT COUNT(*) FROM courses"
    ).fetchone()[0]

    total_facilities = conn.execute(
        "SELECT COUNT(*) FROM facilities"
    ).fetchone()[0]

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_kb = conn.execute(
        "SELECT COUNT(*) FROM knowledge_base"
    ).fetchone()[0]

    return render_template(
        "dashboard_menu.html",
        total_courses=total_courses,
        total_facilities=total_facilities,
        total_students=total_students,
        total_kb=total_kb
    )

# ---------------- LOGOUT ----------------
@admin_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
#                     COURSES MANAGEMENT
# =========================================================

@admin_bp.route("/dashboard/courses")
def courses():

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    courses = conn.execute("SELECT * FROM courses").fetchall()

    specialisations = conn.execute(
        "SELECT s.id, s.specialisation, s.course_id, c.course FROM specialisations s JOIN courses c ON s.course_id=c.id"
    ).fetchall()

    return render_template(
        "courses.html",
        courses=courses,
        specialisations=specialisations
    )


# ADD COURSE
@admin_bp.route("/add_course", methods=["POST"])
def add_course():

    if not session.get("admin"):
        return redirect("/login")

    course = request.form["course"]
    fees = request.form["fees"]
    duration = request.form["duration"]
    eligibility = request.form["eligibility"]

    conn = get_db()

    conn.execute(
        "INSERT INTO courses(course,fees,duration,eligibility) VALUES (?,?,?,?)",
        (course, fees, duration, eligibility)
    )

    conn.commit()

    return redirect("/dashboard/courses")


# DELETE COURSE
@admin_bp.route("/delete_course/<int:id>")
def delete_course(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    conn.execute("DELETE FROM courses WHERE id=?", (id,))
    conn.commit()

    return redirect("/dashboard/courses")
# EDIT COURSE
@admin_bp.route("/edit_course/<int:id>")
def edit_course(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    course = conn.execute(
        "SELECT * FROM courses WHERE id=?",
        (id,)
    ).fetchone()

    return render_template("edit_course.html", course=course)


# UPDATE COURSE
@admin_bp.route("/update_course/<int:id>", methods=["POST"])
def update_course(id):

    if not session.get("admin"):
        return redirect("/login")

    course = request.form["course"]
    fees = request.form["fees"]
    duration = request.form["duration"]
    eligibility = request.form["eligibility"]

    conn = get_db()

    conn.execute(
        "UPDATE courses SET course=?, fees=?, duration=?, eligibility=? WHERE id=?",
        (course, fees, duration, eligibility, id)
    )

    conn.commit()

    return redirect("/dashboard/courses")


# =========================================================
#                 SPECIALISATIONS MANAGEMENT
# =========================================================

@admin_bp.route("/add_specialisation", methods=["POST"])
def add_specialisation():

    if not session.get("admin"):
        return redirect("/login")

    course_id = request.form["course_id"]
    specialisation = request.form["specialisation"]

    conn = get_db()

    conn.execute(
        "INSERT INTO specialisations(course_id,specialisation) VALUES (?,?)",
        (course_id, specialisation)
    )

    conn.commit()

    return redirect("/dashboard/courses")


@admin_bp.route("/delete_specialisation/<int:id>")
def delete_specialisation(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "DELETE FROM specialisations WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect("/dashboard/courses")


# =========================================================
#                 FACILITIES MANAGEMENT
# =========================================================

@admin_bp.route("/dashboard/facilities")
def facilities():

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    facilities = conn.execute("SELECT * FROM facilities").fetchall()

    return render_template("facilities.html", facilities=facilities)


# ADD FACILITY
@admin_bp.route("/add_facility", methods=["POST"])
def add_facility():

    if not session.get("admin"):
        return redirect("/login")

    name = request.form["name"]
    fees = request.form["fees"]
    duration = request.form["duration"]

    conn = get_db()

    conn.execute(
        "INSERT INTO facilities(name,fees,duration) VALUES (?,?,?)",
        (name, fees, duration)
    )

    conn.commit()

    return redirect("/dashboard/facilities")


# DELETE FACILITY
@admin_bp.route("/delete_facility/<int:id>")
def delete_facility(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    conn.execute("DELETE FROM facilities WHERE id=?", (id,))
    conn.commit()

    return redirect("/dashboard/facilities")
#EDIT FACILITY
@admin_bp.route("/edit_facility/<int:id>")
def edit_facility(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    facility = conn.execute(
        "SELECT * FROM facilities WHERE id=?",
        (id,)
    ).fetchone()

    return render_template("edit_facility.html", facility=facility)
#UPDATE FACILITIES
@admin_bp.route("/update_facility/<int:id>", methods=["POST"])
def update_facility(id):

    if not session.get("admin"):
        return redirect("/login")

    name = request.form["name"]
    fees = request.form["fees"]
    duration = request.form["duration"]

    conn = get_db()

    conn.execute(
        "UPDATE facilities SET name=?, fees=?, duration=? WHERE id=?",
        (name, fees, duration, id)
    )

    conn.commit()

    return redirect("/dashboard/facilities")

# =========================================================
#                  STUDENTS MANAGEMENT
# =========================================================

@admin_bp.route("/dashboard/students")
def students():

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    students = conn.execute("SELECT * FROM students").fetchall()

    return render_template("students.html", students=students)


# ADD STUDENT
@admin_bp.route("/add_student", methods=["POST"])
def add_student():

    if not session.get("admin"):
        return redirect("/login")

    username = request.form["username"]
    password = request.form["password"]
    name = request.form["name"]
    email = request.form["email"]

    password_hash = generate_password_hash(password)

    conn = get_db()

    conn.execute(
        "INSERT INTO students(username,password_hash,name,email) VALUES (?,?,?,?)",
        (username, password_hash, name, email)
    )

    conn.commit()

    return redirect("/dashboard/students")


# DELETE STUDENT
@admin_bp.route("/delete_student/<int:id>")
def delete_student(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()

    return redirect("/dashboard/students")


# =========================================================
#                  KNOWLEDGE BASE MANAGEMENT
# =========================================================

@admin_bp.route("/dashboard/knowledge_base")
def knowledge_base():

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    kb_entries = conn.execute(
        "SELECT * FROM knowledge_base"
    ).fetchall()

    return render_template(
        "knowledge_base.html",
        kb_entries=kb_entries
    )


# ADD KNOWLEDGE
@admin_bp.route("/add_kb", methods=["POST"])
def add_kb():

    if not session.get("admin"):
        return redirect("/login")

    question = request.form["question"]
    answer = request.form["answer"]

    conn = get_db()

    conn.execute(
        "INSERT INTO knowledge_base(question,answer) VALUES (?,?)",
        (question, answer)
    )

    conn.commit()

    return redirect("/dashboard/knowledge_base")


# DELETE KNOWLEDGE
@admin_bp.route("/delete_kb/<int:id>")
def delete_kb(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    conn.execute(
        "DELETE FROM knowledge_base WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect("/dashboard/knowledge_base")
#EDIT KNOWLEDGE BASE
@admin_bp.route("/edit_kb/<int:id>")
def edit_kb(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db()

    entry = conn.execute(
        "SELECT * FROM knowledge_base WHERE id=?",
        (id,)
    ).fetchone()

    return render_template("edit_kb.html", entry=entry)
#UPDATE ENTRY ROUTE
@admin_bp.route("/update_kb/<int:id>", methods=["POST"])
def update_kb(id):

    if not session.get("admin"):
        return redirect("/login")

    question = request.form["question"]
    answer = request.form["answer"]

    conn = get_db()

    conn.execute(
        "UPDATE knowledge_base SET question=?, answer=? WHERE id=?",
        (question, answer, id)
    )

    conn.commit()

    return redirect("/dashboard/knowledge_base")