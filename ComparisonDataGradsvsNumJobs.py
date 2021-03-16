import DatabaseWork
import pandas
import plotly

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


def get_database_information_api(database):
    conn, cursor = DatabaseWork.open_db(database)
    cursor.execute("SELECT school_state, student_size_2018 FROM API_University_Data")
    rows = cursor.fetchall()
    DatabaseWork.close_db(conn)
    return rows


def get_database_information_cohort(database):
    conn, cursor = DatabaseWork.open_db(database)
    cursor.execute("SELECT state_name, total_employment, occupation_code FROM XLS_University_Data")
    rows = cursor.fetchall()
    DatabaseWork.close_db(conn)
    return rows


def get_student_size_per_state(database):
    api_student_size_per_state = {}
    states = []
    rows = get_database_information_api(database)
    for row in rows:
        if row[1] is None:
            continue
        elif row[0] not in states:
            api_student_size_per_state[row[0]] = float(row[1]) / 4
            states.append(str(row[0]))
        elif row[0] in states:
            api_student_size_per_state[row[0]] = api_student_size_per_state[row[0]] + float(row[1]) / 4
    return api_student_size_per_state


def get_total_emp_per_state(database):
    xls_total_emp_per_state = {}
    states = []
    rows = get_database_information_cohort(database)
    for row in rows:
        if 30 <= int(row[2][0:2]) <= 49:
            continue
        if row[0] not in states:
            xls_total_emp_per_state[row[0]] = int(row[1])
            states.append(str(row[0]))
        elif row[0] in states:
            xls_total_emp_per_state[row[0]] = xls_total_emp_per_state[row[0]] + int(row[1])
    return xls_total_emp_per_state


def compare_graduates_vs_num_jobs(database):
    comparison = {}
    student_size_per_state = get_student_size_per_state(database)
    employment_per_state = get_total_emp_per_state(database)

    for api_key in student_size_per_state:
        for xls_key in employment_per_state:
            if api_key in inverse and xls_key in us_state_abbrev:
                comparison.update(
                    {api_key: student_size_per_state.get(api_key) / employment_per_state.get(xls_key)})
    return comparison


def get_max_ratio(database):
    descending_sort = sort_descending_order(database)
    return list(descending_sort.values())[0]


def get_min_ratio(database):
    ascending_sort = sort_ascending_order(database)
    return list(ascending_sort.values())[0]


def sort_ascending_order(database):
    return dict(sorted(compare_graduates_vs_num_jobs(database).items(), key=lambda item: item[1]))


def sort_descending_order(database):
    return dict(sorted(compare_graduates_vs_num_jobs(database).items(), key=lambda item: item[1], reverse=True))


def open_map_grads(database):
    # Draw the map and correlate each state to the respective number of universities the state has
    ratio_grads_to_jobs = pandas.Series(compare_graduates_vs_num_jobs(database))

    data = [dict(
        type='choropleth',
        colorscale="BlueRed",
        autocolorscale=False,
        locations=ratio_grads_to_jobs.keys(),
        z=ratio_grads_to_jobs,
        locationmode='USA-states',
        colorbar=dict(
            title="Ratio of College Graduates vs Number of Jobs")
    )]

    layout = dict(
        title='Ratio of College Graduates vs. Number of Jobs Per State',
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True, )
    )
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, filename='NumGrads vs. NumJobs -map.html')
