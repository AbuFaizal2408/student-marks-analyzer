import os
import math
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "student-marks-analyzer-secret-key"

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

# Subjects
SUBJECTS = ["english", "tamil", "maths", "science", "social"]


# Connect to database
def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# Automatically create database and table
def init_db():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT NOT NULL UNIQUE,
                english REAL NOT NULL,
                tamil REAL NOT NULL,
                maths REAL NOT NULL,
                science REAL NOT NULL,
                social REAL NOT NULL,
                total REAL NOT NULL,
                average REAL NOT NULL,
                grade TEXT NOT NULL
            )
        """)


# Grade calculation
def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


# Dashboard and add student
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        roll_number = request.form.get("roll_number", "").strip()

        if not name or not roll_number:
            flash("Please enter student name and roll number.", "error")
            return redirect(url_for("home"))

        marks = []

        try:
            for subject in SUBJECTS:
                mark = float(request.form.get(subject, ""))

                if not math.isfinite(mark) or mark < 0 or mark > 100:
                    raise ValueError

                marks.append(mark)

        except ValueError:
            flash("Enter valid marks between 0 and 100.", "error")
            return redirect(url_for("home"))

        # Calculate total, average and grade
        total = sum(marks)
        average = total / len(SUBJECTS)
        grade = calculate_grade(average)

        try:
            with get_db_connection() as connection:

                connection.execute(
                    """
                    INSERT INTO students (
                        name, roll_number,
                        english, tamil, maths, science, social,
                        total, average, grade
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (name, roll_number, *marks, total, average, grade),
                )

            flash("Student added successfully!", "success")

        except sqlite3.IntegrityError:
            flash("This roll number already exists.", "error")

        return redirect(url_for("home"))

    # Fetch student records
    with get_db_connection() as connection:

        students = connection.execute("""
            SELECT * FROM students
            ORDER BY total DESC, name ASC
        """).fetchall()

        # Total students
        total_students = connection.execute("""
            SELECT COUNT(*) FROM students
        """).fetchone()[0]

        # Class average
        class_average = connection.execute("""
            SELECT AVG(average) FROM students
        """).fetchone()[0]

        # Class topper
        topper = connection.execute("""
            SELECT name, roll_number, total, average, grade
            FROM students
            ORDER BY total DESC, name ASC
            LIMIT 1
        """).fetchone()

    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        class_average=round(class_average, 2) if class_average else 0,
        topper=topper,
    )


# Delete student
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    with get_db_connection() as connection:
        connection.execute("DELETE FROM students WHERE id = ?", (student_id,))

    flash("Student record deleted successfully.", "success")

    return redirect(url_for("home"))


# Initialize database automatically
init_db()


if __name__ == "__main__":
    app.run(debug=True)
