
# Student Marks Analyzer

A web-based student performance management system built using Python, Flask, SQLite, HTML and CSS.

## Features

- Add student details and subject marks.
- Automatically calculate total marks and average.
- Assign grades based on student performance.
- Display class topper.
- Rank students based on total marks.
- View all student records.
- Delete student records.
- Automatically create and manage the SQLite database.
- Responsive dark navy and blue dashboard.

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3

## Project Structure

STUDENT_MARKS_ANALYZER/
- app.py
- database.db
- templates/
  - index.html
- static/
  - style.css

## Installation and Setup

1. Clone this repository.

2. Install Flask:

   pip install flask

3. Run the application:

   python app.py

4. Open your browser and visit:

   http://127.0.0.1:5000

## Grade System

| Average | Grade |
|---|---|
| 90–100 | A+ |
| 80–89 | A |
| 70–79 | B |
| 60–69 | C |
| 50–59 | D |
| Below 50 | F |

## Database

SQLite is used to store student information. The database and students table are automatically created when the application starts.

## Author

Abufaizal
