import pytest
import ApiData
import DatabaseWork


@pytest.fixture
def get_db():
    conn, cursor = DatabaseWork.open_db('test_db_test.sqlite')
    return conn, cursor


@pytest.fixture
def get_demo_job_data():
    test_dict = {'occupation_code': '11-0000',
                 'state_name': "TEST",
                 'occupation_major_title': "Student",
                 'total_employment': 10000,
                 "hourly_25th_salary": 25,
                 "annual_25th_salary": 20000,
                 }
    return test_dict


@pytest.fixture()
def get_demo_api_data():
    test_data = [{'id': 1, 'school.state': 'MA', 'school.name': 'Test University', 'school.city': 'Bridgewater',
                  '2018.student.size': 1000, '2017.student.size': 1001,
                  '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 456,
                  '2016.repayment.3_yr_repayment.overall': 4004,
                  '2016.repayment.repayment_cohort.3_year_declining_balance': 10}]
    return test_data


def test_api_entries():  # Tests to see if more than 1000 entries were obtained
    all_data = ApiData.get_data()
    size = len(all_data)
    assert size >= 1000


def test_university_test(get_db, get_demo_api_data):  # Create new database with test data, and check if the data is in the db
    conn, cursor = get_db
    DatabaseWork.setup_api_db(cursor)
    test_data = get_demo_api_data
    DatabaseWork.populate_api_database(cursor, test_data)
    cursor.execute('''SELECT school_name FROM API_University_Data WHERE school_name = "Test University"''')
    results = cursor.fetchall()
    test_record = results[0]
    DatabaseWork.close_db(conn)
    assert test_record[0] == 'Test University'


def test_data_acquired():  # Tests if data from more than 50 states was obtained
    target_number_states = 50
    states_acquired_xls = []
    workbook = DatabaseWork.openpyxl.load_workbook("CollegeData.xlsx")
    worksheet = workbook.active

    for row in worksheet:
        if row[1].value not in states_acquired_xls:
            states_acquired_xls.append(row[1].value)
    assert len(states_acquired_xls) >= target_number_states


def test_new_table_exist(get_db, get_demo_api_data):  # Tests to see if new table is in database
    target_table = 'XLS_University_Data'
    conn, cursor = get_db

    DatabaseWork.setup_api_db(cursor)
    test_data = get_demo_api_data
    DatabaseWork.populate_api_database(cursor, test_data)

    DatabaseWork.update_db_from_xl("CollegeData.xlsx", cursor)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    DatabaseWork.close_db(conn)

    boolean = False  # Traverse through embedded list of tables, and check if desired one is contained
    for arr in tables:
        if target_table in arr:
            boolean = True

    assert tables and boolean  # Checking to see if tables array exists, and if desired table is in the database


def test_write_to_table(get_db):  # Check to see if Arizona is a state that has a major of Management Occupations
    xls_table_name = 'XLS_University_Data'
    conn, cursor = get_db

    DatabaseWork.setup_xls_db(cursor)
    DatabaseWork.update_db_from_xl("CollegeData.xlsx", cursor)

    cursor.execute(f"SELECT * FROM {xls_table_name} WHERE occupation_major_title LIKE 'Management Occupations'"
                   " AND state_name LIKE 'Arizona'")
    tables = cursor.fetchall()
    DatabaseWork.close_db(conn)
    assert len(tables) == 1  # If we got some data from the excel file
