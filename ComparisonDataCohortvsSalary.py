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
    cursor.execute("SELECT school_state, repayment_3yearDecliningBal_2016 FROM API_University_Data")
    rows = cursor.fetchall()
    DatabaseWork.close_db(conn)
    return rows


def get_database_information_cohort(database):
    conn, cursor = DatabaseWork.open_db("demo_db.sqlite")
    cursor.execute("SELECT state_name, annual_25th_salary FROM XLS_University_Data")
    rows = cursor.fetchall()
    DatabaseWork.close_db(conn)
    return rows


def get_3_year_cohort_decline(database):
    api_3year_decline_per_state = {}
    states = []
    rows = get_database_information_api(database)
    for row in rows:
        if row[1] is None:
            continue
        elif row[0] not in states:
            api_3year_decline_per_state[row[0]] = float(row[1])
        elif row[0] in states:
            api_3year_decline_per_state[row[0]] = api_3year_decline_per_state[row[0]] + float(row[1])
    return api_3year_decline_per_state


def get_25th_percentile_salary(database):
    xls_percentile_salary_per_state = {}
    states = []
    rows = get_database_information_cohort(database)
    for row in rows:
        if row[0] not in states:
            xls_percentile_salary_per_state[row[0]] = int(row[1])
            states.append(str(row[0]))
        elif row[0] in states:
            xls_percentile_salary_per_state[row[0]] = xls_percentile_salary_per_state[row[0]] + int(row[1])
    return xls_percentile_salary_per_state


def compare_cohort_decline_vs_percentile_salary(database):
    comparison = {}
    declining_balance = get_3_year_cohort_decline(database)
    percentile_salary = get_25th_percentile_salary(database)

    for api_key in declining_balance:
        for xls_key in percentile_salary:
            if api_key in inverse and xls_key in us_state_abbrev:
                comparison.update(
                    {api_key: declining_balance.get(api_key) * 1000000 / percentile_salary.get(xls_key)})
    return comparison


def get_max_ratio(database):
    descending_sort = sort_descending_order(database)
    return list(descending_sort.values())[0]


def get_min_ratio(database):
    ascending_sort = sort_ascending_order(database)
    return list(ascending_sort.values())[0]


def sort_ascending_order(database):
    return dict(sorted(compare_cohort_decline_vs_percentile_salary(database).items(), key=lambda item: item[1]))


def sort_descending_order(database):
    return dict(
        sorted(compare_cohort_decline_vs_percentile_salary(database).items(), key=lambda item: item[1], reverse=True))


def open_map_cohort(database):
    # Draw the map and correlate each state to the respective number of universities the state has
    ratio_declining_bal_to_salary = pandas.Series(compare_cohort_decline_vs_percentile_salary(database))

    data = [dict(
        type='choropleth',
        colorscale="BlueRed",
        autocolorscale=False,
        locations=ratio_declining_bal_to_salary.keys(),
        z=ratio_declining_bal_to_salary,
        locationmode='USA-states',
        colorbar=dict(
            title="Ratio of Declining Balance * 10^6 vs 25th Percentile Salary ")
    )]

    layout = dict(
        title='Ratio of Cohort Declining Balance Percentage * 10^6 vs. 25th Percentile Salary Per State',
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True, )
    )
    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, filename='DecliningBal vs. 25%Salary -map.html')
