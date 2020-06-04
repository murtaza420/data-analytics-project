import os, sys, pandas
from datetime import datetime

# Converts string to date
def get_date(d):
    return datetime.strptime(d,'%Y-%m-%d')

# Gets columns dynamically based on no of days and day interval
# No of days is the number of columns represented by days and day interval is the interval between the days
def get_columns(no_of_days, day_interval):
    cols = ['Date', 'County', 'State', 'Population', 'Cases %']
    for i in range(no_of_days):
        cols.append('Cases (N - ' + str((i+1) * day_interval) + ')')
        cols.append('Deaths (N - ' + str((i+1) * day_interval) + ')')
    return cols

# Reads population from the dataframe and saves in a dictionary
# Dictionary: key = county+state (as same county names can be in different states), value = estimated population in 2019
def get_population(df_population):
    population = {}
    for index, row in df_population.iterrows():
        if ('County' in row['CTYNAME']):
            county = row['CTYNAME'][:len(row['CTYNAME']) - 7]
            population.update({ county + row['STNAME']: row['POPESTIMATE2019'] })
    return population

def get_processed_data(population, df_covid, no_of_days, day_interval, start_date, data_len):
    cols = get_columns(no_of_days, day_interval)
    df_data = pandas.DataFrame(columns=cols)
    row_idx = 0
    population_keys = population.keys()
    for index, row in df_covid.iterrows():
        new_row = {}
        date = get_date(row['date'])
        if(date >=  start_date and (row['county'] + row['state']) in population_keys):
            n_data_found = True
            for i in range(no_of_days):
                n_row_idx = row_idx - (i + 1) * day_interval
                if (n_row_idx > 0 and df_covid.iloc[n_row_idx]['county'] == row['county'] and df_covid.iloc[n_row_idx]['state'] == row['state']):
                    new_row.update({ 'Cases (N - ' + str((i+1) * day_interval) + ')': df_covid.iloc[n_row_idx]['cases'] })
                    new_row.update({ 'Deaths (N - ' + str((i+1) * day_interval) + ')': df_covid.iloc[n_row_idx]['deaths'] })
                else:
                    n_data_found = False
                    break
            if (n_data_found):
                new_row.update({ 'Date': row['date'] })
                new_row.update({ 'County': row['county'] })
                new_row.update({ 'State': row['state'] })
                new_row.update({ 'Population': population[new_row['County'] + new_row['State']] })
                new_row.update({ 'Cases %': new_row['Cases (N - ' + str(day_interval) + ')'] / new_row['Population'] * 100 })
                df_data = df_data.append(new_row, ignore_index=True)
        row_idx += 1
        if (row_idx % 100 == 0):
            print(row_idx)
        if(row_idx > data_len):
            break
    return df_data

if __name__ == "__main__":
    df_population = pandas.read_csv('data/co-est2019-alldata.csv', encoding="latin-1")
    df_covid = pandas.read_csv('data/us-counties.txt')
    df_covid = df_covid.sort_values(['state', 'county', 'date'], ascending=[True, True, True])
    day_interval = 7
    no_of_days = 4
    start_date = get_date('2020-02-20')
    
    if (len(sys.argv) > 1):
        day_interval = int(sys.argv[1])
    if (len(sys.argv) > 2):
        no_of_days = int(sys.argv[2])
    if (len(sys.argv) > 3):
        data_len = int(sys.argv[3])
    
    population = get_population(df_population)
    data = get_processed_data(population, df_covid, no_of_days, day_interval, start_date, data_len)

    data.to_csv(r'data/processed_data' + str(data_len) + '.csv')