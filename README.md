# 📚 Library Management System (LMS)

A complete **Flask + SQLite based Library Management System** for managing books, borrowing, returns, overdue records, and fines.

---

## ✨ Features

### 📖 Book Management

* Add books
* View all books
* Delete books
* Track availability

### 🔄 Borrowing System

* Borrow books by **Student ID**
* Automatically sets **due date = 7 days**
* Prevents borrowing unavailable books

### ✅ Return System

* Return borrowed books
* Automatically marks books as available
* Calculates **₱10 per day late fine**

### ⚠️ Overdue Monitoring

* Automatically updates overdue borrowed books
* Shows overdue status in reports

### 📊 Reports

* Borrow logs
* Due dates
* Return dates
* Fine amounts
* Borrow status

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **API Style:** REST API

---

## 📁 Project Structure

```text
lms-system/
│ app.py
│ lms.db
│ requirements.txt
│
├── templates/
│   └── dashboard.html
│
└── static/
    └── style.css
```

---

## ▶️ Installation Guide

### 1) Clone or download the project

```bash
git clone <your-repo-url>
cd lms-system
```

### 2) Install dependencies

```bash
pip install flask
```

### 3) Run the project

```bash
python app.py
```

### 4) Open in browser

```text
http://127.0.0.1:3000/dashboard
```

---

## 🗄️ Database Tables

### 📚 books

| Column    | Type    | Description                 |
| --------- | ------- | --------------------------- |
| id        | INTEGER | Primary key                 |
| title     | TEXT    | Book title                  |
| author    | TEXT    | Book author                 |
| category  | TEXT    | Book category               |
| available | INTEGER | 1 = available, 0 = borrowed |

### 📘 borrow

| Column      | Type    | Description                   |
| ----------- | ------- | ----------------------------- |
| id          | INTEGER | Primary key                   |
| student_id  | TEXT    | Borrower ID                   |
| book_id     | INTEGER | Related book                  |
| borrow_date | TEXT    | Borrow date                   |
| due_date    | TEXT    | Due date                      |
| return_date | TEXT    | Return date                   |
| status      | TEXT    | Borrowed / Returned / Overdue |
| fine        | REAL    | Late fine                     |

---

## 🔌 API Endpoints

### 📚 Books

* `GET /api/books` → Get all books
* `POST /api/books` → Add new book
* `DELETE /api/books/<book_id>` → Delete book

### 🔄 Borrowing

* `POST /api/borrow` → Borrow a book
* `GET /api/borrow` → Get borrow records
* `PUT /api/return/<borrow_id>` → Return a book

### 📊 Reports

* `GET /api/reports` → Get full borrowing report

---

## 💰 Fine Rules

* Borrow period: **7 days**
* Late fine: **₱10 per day**

Example:

* 3 days late = **₱30**
* 5 days late = **₱50**

---

## 🚀 Future Improvements

* User login system
* Librarian/admin roles
* Book search filters
* PDF report export
* Student profile management
* Barcode scanner integration
* Reservation system

---

## 👨‍💻 Developer Notes

This project was built as a **school Library Management System capstone/project prototype**.
It demonstrates:

* CRUD operations
* RESTful API design
* database normalization concepts
* transaction workflow (borrow/return)
* automated fine logic

---

## 📜 License

This project is for **educational purposes only**.


# 🎓 Student Information System (SIS)

A complete **Flask + SQLite based Student Information System** for managing student records, courses, enrollment status, authentication, and dashboard analytics.

---

## ✨ Features

### 👨‍🎓 Student Management

* Add students
* View all students
* Edit student details
* Delete student records
* Search students
* Track enrollment status

### 🔐 Authentication

* Admin login
* Session-based authentication
* Protected dashboard route
* Logout support

### 📊 Dashboard

* Total student count
* Status badges (Active / Terminated)
* Edit modal
* Delete confirmation modal
* Refresh records

### 🔌 REST API

* Full CRUD API for students
* JSON responses
* Supports GET, POST, PUT, PATCH, DELETE

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **API Style:** REST API

---

## 📁 Project Structure

```text
sis-system/
│ app.py
│ database.db
│ requirements.txt
│
├── templates/
│   ├── login.html
│   └── dashboard.html
│
└── static/
    └── style.css
```

---

## ▶️ Installation Guide

### 1) Go to project folder

```bash
cd sis-system
```

### 2) Install dependencies

```bash
pip install flask flask-cors
```

### 3) Run the project

```bash
python app.py
```

### 4) Open in browser

```text
http://127.0.0.1:4000
```

Default login:

* **Username:** `admin`
* **Password:** `1234`

---

## 🗄️ Database Tables

### 👤 users

| Column   | Type | Description    |
| -------- | ---- | -------------- |
| username | TEXT | Primary key    |
| password | TEXT | Login password |

### 🎓 students

| Column | Type | Description           |
| ------ | ---- | --------------------- |
| id     | TEXT | Student ID            |
| name   | TEXT | Full name             |
| course | TEXT | Program/course        |
| status | TEXT | Enrolled / Terminated |

---

## 🔌 API Endpoints

### 👨‍🎓 Students

* `GET /api/students` → Get all students
* `GET /api/students/<student_id>` → Get one student
* `POST /api/students` → Add student
* `PUT /api/students/<student_id>` → Update full record
* `PATCH /api/students/<student_id>` → Update status only
* `DELETE /api/students/<student_id>` → Delete student

### 🔐 Authentication

* `POST /login` → Login
* `GET /logout` → Logout
* `GET /dashboard` → Dashboard page

---

## 🚀 Future Improvements

* Subject management
* Teacher management
* Grades module
* Tuition and payments
* Class schedules
* PDF report export
* Student portal
* Parent access

---

## 👨‍💻 Developer Notes

This project was built as a **Student Information System prototype for academic use**.
It demonstrates:

* CRUD operations
* login authentication
* session handling
* RESTful API design
* dashboard UI integration
* SQLite database design

---

## 📜 License

This project is for **educational purposes

