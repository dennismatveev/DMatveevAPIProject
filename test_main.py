import main
import secrets


def test_entries():  # Tests to see if more than 1000 entries were obtained
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
    main.setup_db(cursor, new_table_name)
    main.populate_database(cursor, all_data, new_table_name)
    cursor.execute("SELECT unique_id FROM " + new_table_name + " WHERE unique_id =" + str(target_unique_id))
    data = cursor.fetchall()
    main.close_db(conn)
    assert target_unique_id == data[0][0]
