from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import time
from datetime import datetime
try:
    from win10toast import ToastNotifier
    notifier = ToastNotifier()
except Exception:
    notifier = None  # allow app to run without win10toast

app = Flask(__name__, template_folder="templates", static_folder="static")

DB_PATH = "students.db"
MIN_INTERVAL = 30  # seconds between submissions from the same IP
last_request_time = {}  # in-memory rate limit store

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name  TEXT NOT NULL,
            dob        TEXT NOT NULL,
            email      TEXT NOT NULL UNIQUE,
            gender     TEXT NOT NULL,
            faculty    TEXT NOT NULL,
            reg_date   TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

@app.route("/")
def index():
    return render_template("Reg.html")

@app.route("/submit", methods=["POST"])
def submit_form():
    ip = request.remote_addr or "unknown"
    now = time.time()

    # simple rate limit
    if ip in last_request_time and now - last_request_time[ip] < MIN_INTERVAL:
        return render_template("error.html", message="Слишком частые регистрации. Попробуйте позже.")

    last_request_time[ip] = now

    first_name = (request.form.get("first_name") or "").strip()
    last_name  = (request.form.get("last_name") or "").strip()
    dob        = (request.form.get("dob") or "").strip()
    email      = (request.form.get("email") or "").strip()
    gender     = (request.form.get("gender") or "").strip()
    faculty    = (request.form.get("faculty") or "").strip()

    # required fields
    if not all([first_name, last_name, dob, email, gender, faculty]):
        return render_template("error.html", message="Пожалуйста, заполните все обязательные поля.")

    # age check
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        return render_template("error.html", message="Некорректная дата рождения.")
    today = datetime.now()
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    if age < 16:
        return render_template("error.html", message="Для регистрации нужно быть старше 16 лет.")

    # save to DB
    try:
        with get_conn() as conn:
            conn.execute(
                """INSERT INTO students (first_name, last_name, dob, email, gender, faculty)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (first_name, last_name, dob, email, gender, faculty)
            )
    except sqlite3.IntegrityError as e:
        # likely duplicate email
        return render_template("error.html", message="Пользователь с таким email уже зарегистрирован.")
    except sqlite3.Error as e:
        return render_template("error.html", message=f"Ошибка базы данных: {e}")

    # Windows toast (only on the machine running the server)
    try:
        if notifier is not None:
            notifier.show_toast(
                "Новая регистрация",
                f"{first_name} {last_name} ({email}) • {faculty}",
                duration=5,
                threaded=True,
                icon_path=None
            )
    except Exception as e:
        print("Toast error:", e)

    return render_template("success.html", name=first_name)

@app.route("/students")
def students():
    try:
        with get_conn() as conn:
            rows = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
        return render_template("students.html", students=rows)
    except sqlite3.Error as e:
        return render_template("error.html", message=f"Ошибка базы данных: {e}")

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    try:
        with get_conn() as conn:
            conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        return redirect(url_for("students"))
    except sqlite3.Error as e:
        return render_template("error.html", message=f"Ошибка базы данных: {e}")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
