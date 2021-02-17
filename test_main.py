import main


def test_entries():
    new_table_name = "University_Test"
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
    all_data = main.get_data(url)
    conn, cursor = main.open_db("demo_db.sqlite")
    main.setup_db(cursor, new_table_name)
    main.populate_database(cursor, all_data, new_table_name)
    main.close_db(conn)

def test_university_test():
    new_table_name = "University_Test"
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
    all_data = main.get_data(url)
    conn, cursor = main.open_db("demo_db.sqlite")
    main.setup_db(cursor, new_table_name)
    main.populate_database(cursor, all_data, new_table_name)
    main.close_db(conn)
    assert