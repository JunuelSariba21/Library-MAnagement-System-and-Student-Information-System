from flask import Flask, request, jsonify, render_template, redirect, session
import sqlite3, requests
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secret123"
CORS(app)

def get_db():
    return sqlite3.connect("database.db")


conn = get_db()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin','1234')")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    available INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS borrow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    book_id TEXT,
    borrow_date TEXT,
    due_date TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

@app.route('/')
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (data['username'], data['password']))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user'] = user[0]
        return redirect('/dashboard')
    return "Invalid login"

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template("dashboard.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/api/books', methods=['GET'])
def get_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([{
        "id": r[0],
        "title": r[1],
        "author": r[2],
        "available": r[3]
    } for r in rows])

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO books VALUES (?, ?, ?, 1)",
                   (data['id'], data['title'], data['author']))

    conn.commit()
    conn.close()
    return jsonify({"message": "Book added"})

@app.route('/api/books/<id>', methods=['PUT'])
def update_book(id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE books SET title=?, author=?, available=? WHERE id=?
    """, (data['title'], data['author'], data['available'], id))

    conn.commit()
    conn.close()
    return jsonify({"message": "Updated"})

@app.route('/api/books/<id>', methods=['DELETE'])
def delete_book(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})


@app.route('/api/borrow', methods=['GET'])
def get_borrow():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM borrow")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([{
        "id": r[0],
        "student_id": r[1],
        "book_id": r[2],
        "borrow_date": r[3],
        "due_date": r[4],
        "status": r[5]
    } for r in rows])

@app.route('/api/borrow', methods=['POST'])
def borrow_book():
    data = request.json


    res = requests.get(f"http://localhost:4000/api/students/{data['student_id']}")
    if res.status_code != 200:
        return jsonify({"message": "Student not found"}), 400

    student = res.json()
    if student['status'] != "Enrolled":
        return jsonify({"message": "Not enrolled"}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT available FROM books WHERE id=?", (data['book_id'],))
    book = cursor.fetchone()

    if not book or book[0] == 0:
        return jsonify({"message": "Book unavailable"}), 400

    cursor.execute("""
    INSERT INTO borrow (student_id, book_id, borrow_date, due_date, status)
    VALUES (?, ?, ?, ?, 'Borrowed')
    """, (data['student_id'], data['book_id'], data['borrow_date'], data['due_date']))

    cursor.execute("UPDATE books SET available=0 WHERE id=?", (data['book_id'],))

    conn.commit()
    conn.close()

    return jsonify({"message": "Borrowed"})

@app.route('/api/borrow/<int:id>', methods=['PATCH'])
def return_book(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT book_id FROM borrow WHERE id=?", (id,))
    book = cursor.fetchone()

    cursor.execute("UPDATE borrow SET status='Returned' WHERE id=?", (id,))

    if book:
        cursor.execute("UPDATE books SET available=1 WHERE id=?", (book[0],))

    conn.commit()
    conn.close()

    return jsonify({"message": "Returned"})

if __name__ == '__main__':
    app.run(port=3000, debug=True)