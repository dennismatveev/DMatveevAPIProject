import main


def test_api_entries():  # Tests to see if more than 1000 entries were obtained
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
    all_data = main.get_data(url)
    size = len(all_data)
    assert size >= 1000


def test_university_test():  # Choose a random target unique id, create the new database and verify the id is present
    target_unique_id = 141802  # Alabama A & M University SchoolCity Normal
    new_table_name = "University_Data"
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
    all_data = main.get_data(url)
    conn, cursor = main.open_db("demo_db_test.sqlite")

    main.setup_api_db(cursor, new_table_name)
    main.populate_api_database(cursor, all_data, new_table_name)
    cursor.execute(f"SELECT unique_id FROM {new_table_name} WHERE unique_id ={str(target_unique_id)}")
    data = cursor.fetchall()
    main.close_db(conn)
    assert data and (target_unique_id == data[0][0])  # Checking if data array exists, if yes then also check actual id







def test_data_acquired():  # Tests if data from more than 50 states was obtained
    target_number_states = 50
    states_acquired_xls = []
    workbook = main.openpyxl.load_workbook("CollegeData.xlsx")
    worksheet = workbook.active

    for row in worksheet:
        if row[1].value not in states_acquired_xls:
            states_acquired_xls.append(row[1].value)
    assert len(states_acquired_xls) >= target_number_states


def test_new_table_exist():  # Tests to see if new table is in database
    target_table = 'XLS_University_Data'
    api_table_name = 'University_Data'
    xls_table_name = 'XLS_University_Data'
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
    all_data = main.get_data(url)
    conn, cursor = main.open_db("demo_db.sqlite")

    main.setup_api_db(cursor, api_table_name)
    main.populate_api_database(cursor, all_data, api_table_name)

    main.setup_xls_db(cursor, xls_table_name)
    workbook = main.openpyxl.load_workbook("CollegeData.xlsx")
    worksheet = workbook.active
    main.populate_xls_db(cursor, worksheet, xls_table_name)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    main.close_db(conn)

    boolean = False  # Traverse through embedded list of tables, and check if desired one is contained
    for arr in tables:
        if target_table in arr:
            boolean = True

    assert tables and boolean  # Checking to see if tables array exists, and if desired table is in the database


def test_old_table_exists():  # Tests to see if old table still exists in database
    target_table = 'University_Data'
    api_table_name = 'University_Data'
    xls_table_name = 'XLS_University_Data'
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
    all_data = main.get_data(url)
    conn, cursor = main.open_db("demo_db.sqlite")

    main.setup_api_db(cursor, api_table_name)
    main.populate_api_database(cursor, all_data, api_table_name)

    main.setup_xls_db(cursor, xls_table_name)
    workbook = main.openpyxl.load_workbook("CollegeData.xlsx")
    worksheet = workbook.active
    main.populate_xls_db(cursor, worksheet, xls_table_name)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    main.close_db(conn)

    boolean = False  # Traverse through embedded list of tables, and check if desired one is contained
    for arr in tables:
        if target_table in arr:
            boolean = True

    assert tables and boolean  # Checking to see if tables array exists, and if desired table is in the database


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
