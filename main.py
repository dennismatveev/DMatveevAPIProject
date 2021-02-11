import requests
import secrets
import time
import math
import sqlite3
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS students(
    banner_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gpa REAL DEFAULT 0,
    credits INTEGER DEFAULT 0
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS course(
    course_prefix TEXT NOT NULL,
    course_number INTEGER NOT NULL,
    cap INTEGER DEFAULT 20,
    description TEXT,
    PRIMARY KEY(course_prefix, course_number)
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS class_list(
       registration_id INTEGER PRIMARY KEY,
       course_prefix TEXT NOT NULL,
       course_number INTEGER NOT NULL,
       banner_id INTEGER NOT NULL,
       registration_date TEXT,
       FOREIGN KEY (banner_id) REFERENCES student (banner_id)
       ON DELETE CASCADE ON UPDATE NO ACTION,
       FOREIGN KEY (course_prefix, course_number) REFERENCES courses (course_prefix, course_number)
       ON DELETE CASCADE ON UPDATE NO ACTION
       );''')

def main():
    conn, cursor = open_db("demo_db.sqlite")
    print(type(conn))
    setup_db(cursor)
    close_db(conn)

# def main():
#
#     url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
#     all_data = get_data(url)
# dont need    with open('College_data.txt', 'w') as f:
# dont need        print(all_data, file=f)


if __name__ == '__main__':
    main()
