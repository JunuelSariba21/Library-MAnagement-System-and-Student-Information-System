from flask import Flask, request, jsonify, render_template, redirect, session
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secret123"
CORS(app)

DB = "database.db"


# =========================
# DATABASE CONNECTION
# =========================
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# INITIALIZE DATABASE
# =========================
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)

    # DEFAULT ADMIN
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password)
    VALUES ('admin', '1234')
    """)

    # STUDENTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        course TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# AUTH ROUTES
# =========================
@app.route('/')
def login_page():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        session["user"] = user["username"]
        return redirect("/dashboard")

    return "Invalid login credentials"


@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


# =========================
# STUDENT API ROUTES
# =========================
@app.route('/api/students', methods=['GET'])
def get_students():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students ORDER BY name ASC")
    students = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "student_id": s["id"],
            "name": s["name"],
            "course": s["course"],
            "status": s["status"]
        }
        for s in students
    ])


@app.route('/api/students/<student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    s = cursor.fetchone()
    conn.close()

    if not s:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({
        "student_id": s["id"],
        "name": s["name"],
        "course": s["course"],
        "status": s["status"]
    })


@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data received"}), 400

    required = ["student_id", "name", "course", "status"]
    for field in required:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students (id, name, course, status)
    VALUES (?, ?, ?, ?)
    """, (
        data["student_id"],
        data["name"],
        data["course"],
        data["status"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Student added successfully"})

@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students
    SET name=?, course=?, status=?
    WHERE id=?
    """, (
        data["name"],
        data["course"],
        data["status"],
        student_id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Student updated successfully"})


@app.route('/api/students/<student_id>', methods=['PATCH'])
def patch_student(student_id):
    data = request.get_json()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students
    SET status=?
    WHERE id=?
    """, (
        data["status"],
        student_id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Student status updated"})


@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted successfully"})


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True, port=4000)