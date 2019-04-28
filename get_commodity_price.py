"""Get commodity price's mean and variance from local csv data in a date range

Currently, the program supports gold and silver commodities, corresponding to gold.csv and silver.csv, respectively
The data in csv files have Date and Price colums

Example:
        $ python get_commodity_price.py 2019-04-01 2019-04-26

"""

import sys

import pandas as pd


def read_csv(csv_file):
    return pd.read_csv(csv_file)


def main(start, end, commodity):
    ''' According to start and end dates, read the corresponding csv data and calculate the mean and variance
    '''

    if commodity.lower() == 'gold':
        df = read_csv('gold.csv')
    elif commodity.lower() == 'silver':
        df = read_csv('silver.csv')
    else:
        df = pd.DataFrame()
        raise Exception('Commodity can only be gold or silver')

    df['Date'] = pd.to_datetime(df['Date'])

    try:
        # Replace comma in the numbers
        df['Price'] = pd.to_numeric(df['Price'].str.replace(',', ''))
    except AttributeError:
        df['Price'] = pd.to_numeric(df['Price'])

    try:
        mask = (df['Date'] > start) & (df['Date'] <= end)
        data_in_range = df.loc[mask]
        # check if data is empty
        if not data_in_range.empty:
            mean = data_in_range['Price'].mean()
            var = data_in_range['Price'].var()

            # print the result
            print commodity, "{0:.2f}".format(mean), "{0:.2f}".format(var)
        else:
            print('No data in the specified date range')

    except TypeError as error:
        print(error)
        print('The Date format is incorrect!')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage: python get_commodity_price.py start_date end_date commodity")
        exit(-1)
    else:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
        commodity = sys.argv[3]

        main(start_date, end_date, commodity)
