import requests
import secrets
import time
import math
import sqlite3
import random
from typing import Tuple


def get_data(url: str):
    total_items = 3203
    items_per_page = 20
    # Which fields are desired in the output
    fields = ["school.name,", "school.city,", "2018.student.size,", "2017.student.size,",
              "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,",
              "2016.repayment.3_yr_repayment.overall"
              ]
    # this will hold the return value
    all_data = []

    # Convert List to  String
    field_string = ''.join(fields)

    # Loop through amount of pages and get all data points from each page
    for pages in range(0, math.ceil(total_items/items_per_page)):
        full_url = f"{url}{field_string}&api_key={secrets.api_key}&page={pages}"
        response = requests.get(full_url)
        if response.status_code != 200:
            print(response.text)
            return []
        json_data = response.json()
        results = json_data['results']
        all_data.extend(results)
        time.sleep(.05)
    return all_data


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)#connect to existing DB or create new one
    cursor = db_connection.cursor()#get ready to read/write data
    return db_connection, cursor


def close_db(connection:sqlite3.Connection):
    connection.commit()#make sure any changes get saved
    connection.close()

def setup_db(cursor:sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS University_Data(
    school_name TEXT NOT NULL PRIMARY KEY,
    school_city TEXT NOT NULL,
    student_size_2018 INTEGER DEFAULT 0,
    student_size_2017 INTEGER DEFAULT 0,
    earnings_after3yearscompletion_2017 INTEGER DEFAULT 0,
    repayment_3years_2016 INTEGER DEFAULT 0
    );''')

    # cursor.execute('''CREATE TABLE IF NOT EXISTS students(
    # banner_id INTEGER PRIMARY KEY,
    # first_name TEXT NOT NULL,
    # last_name TEXT NOT NULL,
    # gpa REAL DEFAULT 0,
    # credits INTEGER DEFAULT 0
    # );''')
    # cursor.execute('''CREATE TABLE IF NOT EXISTS course(
    # course_prefix TEXT NOT NULL,
    # course_number INTEGER NOT NULL,
    # cap INTEGER DEFAULT 20,
    # description TEXT,
    # PRIMARY KEY(course_prefix, course_number)
    # );''')
    # cursor.execute('''CREATE TABLE IF NOT EXISTS class_list(
    #    registration_id INTEGER PRIMARY KEY,
    #    course_prefix TEXT NOT NULL,
    #    course_number INTEGER NOT NULL,
    #    banner_id INTEGER NOT NULL,
    #    registration_date TEXT,
    #    FOREIGN KEY (banner_id) REFERENCES student (banner_id)
    #    ON DELETE CASCADE ON UPDATE NO ACTION,
    #    FOREIGN KEY (course_prefix, course_number) REFERENCES courses (course_prefix, course_number)
    #    ON DELETE CASCADE ON UPDATE NO ACTION
    #    );''')

def make_initial_students(cursor: sqlite3.Cursor):
    cursor.execute(f'''INSERT INTO STUDENTS (banner_id, first_name, last_name, gpa, credits)
            VALUES (1001, "John", "Santore", ?, ?)''', (random.uniform(0.0, 4.0), random.randint(0, 120))) # This is important- use with loop
    cursor.execute(f'''INSERT INTO STUDENTS(banner_id, first_name, last_name, gpa, credits)
            VALUES(1002, "Enping", "Li", {random.uniform(0.0, 4.0)}, {random.randint(0, 120)})''')
    cursor.execute(f'''INSERT INTO STUDENTS(banner_id, first_name, last_name, gpa, credits)
            VALUES(1003, "Michael", "Black", {random.uniform(0.0, 4.0)}, {random.randint(0, 120)})''')
    cursor.execute(f'''INSERT INTO STUDENTS(banner_id, first_name, last_name, gpa, credits)
            VALUES(1004, "Seikyung", "Jung", {random.uniform(0.0, 4.0)}, {random.randint(0, 120)})''')
    cursor.execute(f'''INSERT INTO STUDENTS(banner_id, first_name, last_name, gpa, credits)
            VALUES(1005, "Haleh", "Khojasteh", {random.uniform(0.0, 4.0)}, {random.randint(0, 120)})''')

def make_initial_courses(cursor:sqlite3.Cursor):
    cursor.execute(f'''INSERT INTO COURSE (course_prefix, course_number, cap, description)
        VALUES ('COMP', 151, 24, 'This is the intro course, you will learn to program, maybe for the first time')''')
    cursor.execute(f'''INSERT INTO COURSE (course_prefix, course_number, cap, description)
        VALUES ('COMP', 490, 20, 'This is the final course. You will get a chance to apply much of what you learned troughout the undergrad degree')''')
    cursor.execute(f'''INSERT INTO COURSE (course_prefix, course_number, cap, description)
        VALUES ('MATH', 130, 20, 'This course is changing to include much more on graph theory and number bases/systems')''')

def make_initial_classLists(cursor: sqlite3.Cursor):
    cursor.execute(f'''INSERT INTO CLASS_LIST (banner_id, course_prefix, course_number,  registration_date)
    VALUES(1001, 'Comp', 490, DATE('now'))
    ''')
    cursor.execute(f'''INSERT INTO CLASS_LIST (banner_id, course_prefix, course_number,  registration_date)
        VALUES(1002, 'Comp', 490, DATE('now'))
        ''')
    cursor.execute(f'''INSERT INTO CLASS_LIST (banner_id, course_prefix, course_number,  registration_date)
            VALUES(1003, 'Comp', 490, DATE('now'))
            ''')
    cursor.execute(f'''INSERT INTO CLASS_LIST (banner_id, course_prefix, course_number,  registration_date)
            VALUES(1004, 'Comp', 490, DATE('now'))
            ''')
    cursor.execute(f'''INSERT INTO CLASS_LIST (banner_id,  course_prefix, course_number, registration_date)
            VALUES(1005, 'Comp', 490, DATE('now'))
            ''')

def show_simple_select(cursor:sqlite3.Cursor):
    cutoff = float(input("What should the GPA cutoff be?"))
    #question to class-what about security issues here? 	       #Discuss
    result = cursor.execute(f'SELECT * from STUDENTS WHERE gpa < {cutoff}')
    for row in result:
        print(f'BannerId: {row[0]}\nName: {row[1]}\
             {row[2]}\nGPA:{row[3]}')

def main():
    conn, cursor = open_db("demo_db.sqlite")
    #print(type(conn))
    #make_initial_students(cursor)
    #make_initial_courses(cursor)
    #make_initial_classLists(cursor)
    setup_db(cursor)
    #show_simple_select(cursor)
    close_db(conn)

# def main():
#
#     url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
#     all_data = get_data(url)
# dont need    with open('College_data.txt', 'w') as f:
# dont need        print(all_data, file=f)


if __name__ == '__main__':
    main()
