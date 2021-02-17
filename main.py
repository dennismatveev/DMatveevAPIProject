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
    fields = ["id,", "school.name,", "school.city,", "2018.student.size,", "2017.student.size,",
              "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,",
              "2016.repayment.3_yr_repayment.overall"
              ]
    # this will hold the return value
    all_data = []

    # Convert List to  String
    field_string = ''.join(fields)

    # Loop through amount of pages and get all data points from each page
    for pages in range(0, math.ceil(total_items / items_per_page)):
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
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


# make the database and assign the fields
def setup_db(cursor: sqlite3.Cursor, table_name):
    cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (
    unique_id INTEGER PRIMARY KEY,
    school_name TEXT NOT NULL,
    school_city TEXT NOT NULL,
    student_size_2018 INTEGER DEFAULT 0,
    student_size_2017 INTEGER DEFAULT 0,
    earnings_after3yearscompletion_2017 INTEGER DEFAULT 0,
    repayment_3years_2016 INTEGER DEFAULT 0
    );''')


# Populate database
def populate_database(cursor: sqlite3.Cursor, all_data, table_name):
    cursor.execute(f''' DELETE FROM ''' + table_name)  # Deletes table, to ensure no data is left over

    for element in all_data:  # Traverse through all data from API and place it into the correct field

        cursor.execute(f'''INSERT INTO ''' + table_name + ''' (unique_id, school_name, school_city, student_size_2018, student_size_2017,
                                                earnings_after3yearscompletion_2017, repayment_3years_2016)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', (element['id'], element['school.name'], element['school.city'],
                                                  element['2018.student.size'], element['2017.student.size'],
                                                  element['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
                                                  element['2016.repayment.3_yr_repayment.overall']))


def main():
    table_name = 'University_Data'
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
    all_data = get_data(url)
    conn, cursor = open_db("demo_db.sqlite")
    setup_db(cursor, table_name)
    populate_database(cursor, all_data, table_name)
    close_db(conn)


if __name__ == '__main__':
    main()
