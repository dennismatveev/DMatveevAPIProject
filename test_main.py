import pytest
import ApiData
import DatabaseWork
import GuiWindow


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

def test_api_entries():  # Tests to see if more than 1000 entries were obtained
    all_data = ApiData.get_data()
    size = len(all_data)
    assert size >= 1000


def test_university_test(
        get_db):  # Choose a random target unique id, create the new database and verify the id is present
    # first lets add test data
    conn, cursor = get_db
    DatabaseWork.setup_api_db(cursor)
    test_data = [{'id': 1, 'school.state': 'MA', 'school.name': 'Test University', 'school.city': 'Bridgewater',
                  '2018.student.size': 1000, '2017.student.size': 1001,
                  '2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line': 456,
                  '2016.repayment.3_yr_repayment.overall': 4004,
                  '2016.repayment.repayment_cohort.3_year_declining_balance': 10}]
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


# def test_new_table_exist():  # Tests to see if new table is in database
#     target_table = 'XLS_University_Data'
#     api_table_name = 'University_Data'
#     xls_table_name = 'XLS_University_Data'
#     url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
#     all_data = main.get_data(url)
#     conn, cursor = main.open_db("demo_db.sqlite")
#
#     main.setup_api_db(cursor, api_table_name)
#     main.populate_api_database(cursor, all_data, api_table_name)
#
#     main.setup_xls_db(cursor, xls_table_name)
#     workbook = main.openpyxl.load_workbook("CollegeData.xlsx")
#     worksheet = workbook.active
#     main.populate_xls_db(cursor, worksheet, xls_table_name)
#
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     tables = cursor.fetchall()
#     main.close_db(conn)
#
#     boolean = False  # Traverse through embedded list of tables, and check if desired one is contained
#     for arr in tables:
#         if target_table in arr:
#             boolean = True
#
#     assert tables and boolean  # Checking to see if tables array exists, and if desired table is in the database
#
#
# def test_old_table_exists():  # Tests to see if old table still exists in database
#     target_table = 'University_Data'
#     api_table_name = 'University_Data'
#     xls_table_name = 'XLS_University_Data'
#     url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
#     all_data = main.get_data(url)
#     conn, cursor = main.open_db("demo_db.sqlite")
#
#     main.setup_api_db(cursor, api_table_name)
#     main.populate_api_database(cursor, all_data, api_table_name)
#
#     main.setup_xls_db(cursor, xls_table_name)
#     workbook = main.openpyxl.load_workbook("CollegeData.xlsx")
#     worksheet = workbook.active
#     main.populate_xls_db(cursor, worksheet, xls_table_name)
#
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     tables = cursor.fetchall()
#     main.close_db(conn)
#
#     boolean = False  # Traverse through embedded list of tables, and check if desired one is contained
#     for arr in tables:
#         if target_table in arr:
#             boolean = True
#
#     assert tables and boolean  # Checking to see if tables array exists, and if desired table is in the database



def test_write_to_table():  # Check to see if Arizona is a state that has a major of Management Occupations

    target_state_name = 'Arizona'
    xls_table_name = 'XLS_University_Data'
    conn, cursor = main.open_db("demo_db.sqlite")

    main.setup_xls_db(cursor, xls_table_name)
    workbook = main.openpyxl.load_workbook("CollegeData.xlsx")
    worksheet = workbook.active
    main.populate_xls_db(cursor, worksheet, xls_table_name)

    cursor.execute(f"SELECT * FROM {xls_table_name} WHERE occupation_major_title LIKE 'Management Occupations'"
                   " AND state_name LIKE 'Arizona'")
    tables = cursor.fetchall()
    main.close_db(conn)
    assert len(tables) == 1  # If we got some data from the excel file

    # Go through the nested list, to see if the target state is included in the states with that major
    is_exist = False
    for nested_data in tables:
        if target_state_name in nested_data:
            is_exist = True
    assert is_exist
