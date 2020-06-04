# Prediction of new COVID19 spots

## Dataset
Two datasets are used in this project:
1. County wise COVID19 data: https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv
- Save the data in .txt format
2. County wise population: https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/

Move both the data files to data/ folder

## Prerequisites

Run the following command to download all the dependencies

```
pip install -r requirements.txt
```

## Data preprocessing

### Approach

- The data is preprocessed to merge the population and COVID19 cases for each county.
- N features are also created based on number of cases and number of deaths on past data
- For example, you can create additional features (cases and deaths) for past 4 weeks or past 14 days

### Running the script

The script takes 3 optional arguments:
1. day_interval - 7 (if weekly data is desired)
2. no_of_days - 4 (if no of instances desired is 4)
3. data_len - 10000 (if only 10000 rows need to be parsed in the data)

The values mentioned above will be taken as default if no arguments are provided. 

If you want to parse the whole data, set data_len = -1

You can change the value of the parameters based on your requirements.

Run without arguments
```
python preprocess.py
```

Run with arguments (for past 4 weeks)
```
python preprocess.py 7 4 10000
```

Run with arguments (for past 14 days)
```
python preprocess.py 1 14 10000
```
