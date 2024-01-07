import datetime
import random
import sqlite3
from pathlib import Path
from datetime import date
import faker
import os


def time_delta(start, stop):
    res = []
    current_date: datetime = start
    while current_date <= stop:
        if current_date.datetime.isoweekday() < 6:
            res.append(current_date)
        current_date += datetime.timedelta(1)
    return res


def db_constructor(path: Path):
    if not path.exists(F"{os.path.basename(path).split(".")[0]}.db"):
        with open(path) as file:
            sql = file.read()
        with sqlite3.connect(F"{os.path.basename(path).split(".")[0]}.db") as connection:
            curs = connection.cursor()
            curs.executescript(sql)
            connection.commit()


def insert_data():
    disciplines = ["Волоконно-оптичні лінії зв'язку", "ІВНБ", "Веб - програмування", "Системне програмування",
                   "Моделювання та оптимізація систем та мереж телекомунікацій", "Інтелектуальна власність та ліцензування програмного забезпечення",
                   "Телекомунікаційні системи мереж наступного покоління", "Технології самоподібних систем"]
    
    groups = ["501-TT", "501-TH", "501-TK", "401-ME"]

    fake_data = faker.Faker("uk-UA")
    connection = sqlite3.connect("students.db")
    curs = connection.cursor()
    teachers_count = 6
    students_count = 64

    def generate_teachers():
        teachers = []

        for i in range(teachers_count):
            teachers.append(fake_data.name())
        sql_teachers = 'INSERT INTO teachers(fullname) VALUES (?)'
        curs.executemany(sql_teachers, zip(teachers, ))
    

    def generate_disciplines():
        sql_disciplines = 'INSERT INTO disciplines(name, teacher_id) VALUES (?, ?)'
        curs.executemany(
            sql_disciplines,
            zip(
                disciplines, iter(random.randint(1, teachers_count) for i in range(len(disciplines)))
            )
        )
    
    def generate_group():
        sql_groups = 'INSERT INTO groups(name) VALUES (?)'
        curs.executemany(sql_groups, zip(groups, ))
    
    def generate_students():
        students = []
        for i in range(students_count):
            students.append(fake_data.name())
        sql_students = 'INSERT INTO students(fullname, group_id) VALUES (?,?)'
        curs.executemany(sql_students, zip(students, iter(random.randint(1, len(groups)) for i in range(len(students)))))
    
    def generate_grades():
        start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2023-05-25", "%Y-%m-%d")
        d_range = time_delta()

        grades = []

        for i in grades:
            random_discipline = random.randint(1, len(disciplines))
            random_students = [random.randint(1, students_count) for i in range(3)]
            for student in random_students:
                grades.append((student, random_discipline, i.date(), random.randint(1, 12)))
        sql_rating = 'INSERT INTO grades(student_id, discipline_id, date_of, grade) VALUES (?, ?, ?, ?)'
        curs.executemany(sql_rating, grades)



    generate_teachers()
    generate_disciplines()
    generate_group()
    generate_students()
    generate_grades()
    connection.commit()
    connection.close()

if __name__ == "__main__":
    db_constructor("students.db")
    insert_data()