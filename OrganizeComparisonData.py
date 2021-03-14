import ApiData
import DatabaseWork

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
inverse = {v: k for k, v in us_state_abbrev.items()}
api_student_size_per_state = {}
xls_total_emp_per_state = {}
comparison = {}


def get_student_size_per_state():
    states = []
    conn, cursor = DatabaseWork.open_db("demo_db.sqlite")
    cursor.execute("SELECT school_state, student_size_2018 FROM API_University_Data")
    tables = cursor.fetchall()
    DatabaseWork.close_db(conn)
    for table in tables:
        if table[1] is None:
            continue
        elif table[0] not in states:
            api_student_size_per_state.update({str(table[0]): table[1]})
            states.append(str(table[0]))
        elif table[0] in states:
            api_student_size_per_state[table[0]] = api_student_size_per_state[table[0]] + int(table[1])


def get_total_emp_per_state():
    states = []
    conn, cursor = DatabaseWork.open_db("demo_db.sqlite")
    cursor.execute("SELECT state_name, total_employment FROM XLS_University_Data")
    tables = cursor.fetchall()
    DatabaseWork.close_db(conn)
    for table in tables:
        if table[0] not in states:
            xls_total_emp_per_state.update({str(table[0]): table[1]})
            states.append(str(table[0]))
        elif table[0] in states:
            xls_total_emp_per_state[table[0]] = xls_total_emp_per_state[table[0]] + int(table[1])


# Sort Ascend & Descend using _____.sort() vs _____.sort(reverse=True)
def compare_graduates_vs_num_jobs(type_display: str):
    get_student_size_per_state()
    get_total_emp_per_state()

    for api_key in api_student_size_per_state:
        for xls_key in xls_total_emp_per_state:
            counter = 0
            if api_key in inverse and xls_key in us_state_abbrev:
                comparison.update(
                    {api_key: api_student_size_per_state.get(api_key) / xls_total_emp_per_state.get(xls_key)})
            counter += 1

    if type_display == "a":
        ascending_sort = dict(sorted(comparison.items(), key=lambda item: item[1]))
        return ascending_sort
    elif type_display == "d":
        descending_sort = dict(sorted(comparison.items(), key=lambda item: item[1], reverse=True))
        return descending_sort
