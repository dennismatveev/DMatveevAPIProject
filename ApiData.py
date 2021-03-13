import requests
import secrets
import time


def get_data():
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
    # Which fields are desired in the output
    fields = ["id,", "school.state,", "school.name,", "school.city,", "2018.student.size,", "2017.student.size,",
              "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,",
              "2016.repayment.3_yr_repayment.overall,", "2016.repayment.repayment_cohort.3_year_declining_balance"
              ]
    # this will hold the return value
    all_data = []

    # Convert List to  String
    field_string = ''.join(fields)

    # Get the first page from API
    response = requests.get(f"{url}{field_string}&api_key={secrets.api_key}")
    first_page = response.json()
    if response.status_code != 200:
        print(F"Error Getting Data from API: {response.raw}")
        return []
    total_results = first_page['metadata']['total']
    page = 0
    per_page = first_page['metadata']['per_page']
    all_data.extend(first_page['results'])
    while (page + 1) * per_page < total_results:  # Loop through all pages until all data is collected
        page += 1
        response = requests.get(f"{url}{field_string}&api_key={secrets.api_key}&page={page}")
        if response.status_code != 200:  # if we didn't get good data keep going
            continue
        current_page = response.json()
        all_data.extend(current_page['results'])
        time.sleep(.05)

    return all_data
