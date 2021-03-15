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
api_3year_decline_per_state = {}
xls_percentile_salary_per_state = {}
comparison = {}


def get_3_year_cohort_decline():
    states = []
    conn, cursor = DatabaseWork.open_db("demo_db.sqlite")
    cursor.execute("SELECT school_state, repayment_3yearDecliningBal_2016 FROM API_University_Data")
    rows = cursor.fetchall()
    DatabaseWork.close_db(conn)
    for row in rows:
        if row[1] is None:
            continue
        elif row[0] not in states:
            api_3year_decline_per_state[row[0]] = float(row[1])
        elif row[0] in states:
            api_3year_decline_per_state[row[0]] = api_3year_decline_per_state[row[0]] + float(row[1])


def get_25th_percentile_salary():
    states = []
    conn, cursor = DatabaseWork.open_db("demo_db.sqlite")
    cursor.execute("SELECT state_name, annual_25th_salary FROM XLS_University_Data")
    rows = cursor.fetchall()
    DatabaseWork.close_db(conn)
    for row in rows:
        if row[0] not in states:
            xls_percentile_salary_per_state[row[0]] = int(row[1])
            states.append(str(row[0]))
        elif row[0] in states:
            xls_percentile_salary_per_state[row[0]] = xls_percentile_salary_per_state[row[0]] + int(row[1])


def compare_cohort_decline_vs_percentile_salary():
    get_3_year_cohort_decline()
    get_25th_percentile_salary()

    for api_key in api_3year_decline_per_state:
        for xls_key in xls_percentile_salary_per_state:
            if api_key in inverse and xls_key in us_state_abbrev:
                comparison.update(
                    {api_key: api_3year_decline_per_state.get(api_key) / xls_percentile_salary_per_state.get(xls_key)})


def sort_ascending_order():
    return dict(sorted(comparison.items(), key=lambda item: item[1]))


def sort_descending_order():
    return dict(sorted(comparison.items(), key=lambda item: item[1], reverse=True))
