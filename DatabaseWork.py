import sqlite3
import openpyxl
from typing import Tuple


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def setup_api_db(cursor: sqlite3.Cursor):  # make the database and assign the fields
    table_name = "API_University_Data"
    cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (
    unique_id INTEGER PRIMARY KEY,
    school_state TEXT NOT NULL,
    school_name TEXT NOT NULL,
    school_city TEXT NOT NULL,
    student_size_2018 INTEGER DEFAULT 0,
    student_size_2017 INTEGER DEFAULT 0,
    earnings_after3yearscompletion_2017 INTEGER DEFAULT 0,
    repayment_3years_2016 INTEGER DEFAULT 0,
    repayment_3yearDecliningBal_2016 REAL Default 0
    );''')


def populate_api_database(cursor: sqlite3.Cursor, all_data):  # Populate database
    table_name = "API_University_Data"
    cursor.execute(f''' DELETE FROM {table_name}''')  # Deletes table, to ensure no data is left over

    for element in all_data:  # Traverse through all data from API and place it into the correct field

        cursor.execute(f'''INSERT INTO {table_name} (unique_id, school_state, school_name, school_city,
                                                    student_size_2018, student_size_2017,
                                                    earnings_after3yearscompletion_2017,
                                                    repayment_3years_2016, repayment_3yearDecliningBal_2016)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (element['id'], element['school.state'], element['school.name'],
                                                        element['school.city'],
                                                        element['2018.student.size'], element['2017.student.size'],
                                                        element['2017.earnings.3_yrs_after_completion'
                                                                '.overall_count_over_poverty_line'],
                                                        element['2016.repayment.3_yr_repayment.overall'],
                                                        element['2016.repayment.repayment_cohort'
                                                                '.3_year_declining_balance']))


def setup_xls_db(cursor: sqlite3.Cursor):
    table_name = "XLS_University_Data"
    cursor.execute('''CREATE TABLE IF NOT EXISTS ''' + table_name + ''' (
    occupation_code TEXT,
    state_name TEXT,
    occupation_major_title TEXT NOT NULL,
    total_employment INTEGER DEFAULT 0,
    hourly_25th_salary INTEGER DEFAULT 0,
    annual_25th_salary INTEGER DEFAULT 0,
    PRIMARY KEY(occupation_code,state_name)
    );''')


def populate_xls_db(cursor: sqlite3.Cursor, ws, xls_table_name):  # Populates database with data from excel file
    cursor.execute(f''' DELETE FROM {xls_table_name}''')  # Deletes table, to ensure no data is left over

    for row in ws:
        if row[9].value == 'major':  # If the group is 'major' then acquire the data associated with it

            cursor.execute(f'''INSERT INTO {xls_table_name} (occupation_code, state_name, occupation_major_title,
                                                            total_employment, hourly_25th_salary, annual_25th_salary)
                VALUES (?, ?, ?, ?, ?, ?)''', (row[7].value, row[1].value, row[8].value, row[10].value, row[19].value,
                                               row[24].value))


def update_db_from_xl(filename: str, cursor: sqlite3.Cursor):
    table_name = "XLS_University_Data"
    workbook = openpyxl.load_workbook(filename)
    worksheet = workbook.active
    populate_xls_db(cursor, worksheet, table_name)
