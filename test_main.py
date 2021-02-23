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


def test_data_acquired():
    target_number_states = 50
    states_acquired_xls = []
    workbook = main.openpyxl.load_workbook("CollegeData.xlsx")
    worksheet = workbook.active

    for row in worksheet:
        if row[1].value not in states_acquired_xls:
            states_acquired_xls.append(row[1].value)
    assert len(states_acquired_xls) >= target_number_states


def test_new_table_created():
    pass  # Make sure they is a new table


def test_old_table_exists():
    pass  # Make sure original table is still there


def test_write_to_table():
    pass  # double check it actually wrote the right data
