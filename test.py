import sqlite3


with sqlite3.connect("students.db") as connect:
    curs = connect.cursor()

    curs.execute(
        """CREATE TABLE students (
        student_id INTEGER,
        student_name TEXT,
        student_fname TEXT,
        student_group INTEGER
        )"""
    )