import requests
import secrets
import time
import math


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


def main():

    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
    all_data = get_data(url)
    with open('College_data.txt', 'w') as f:
        print(all_data, file=f)


if __name__ == '__main__':
    main()