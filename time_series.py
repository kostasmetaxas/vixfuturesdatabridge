import pandas as pd
import numpy as np
import datetime
import glob
import csv

#Date format: Year-Month-Day
date_format ='%Y-%m-%d'



# USE THESE AS DEFAULTS IF NO ARGUMENTS
# first_target_contract = "2013-01-16"
#
# roll_days = 0
#
# forward = 1



# first_target_contract: First contract in time series for which VIX curve is calculated. Input in '%Y-%m-%d' format.
# roll_days: Amount of days ,before current contract expiration, roll to the next contract.
# forward: Refers to the VX<forward>. Example: if forward=2 calculate VX2 curve.
def generate_time_series(first_target_contract, roll_days, forward):

    # TODO DEFAULT VALUES IF EMPTY PARAMS

    # Create new .csv file where time series data will be inserted.
    file_name = first_target_contract + '_' + roll_days + '_' + forward + '_Time_Series.csv'
    last_date = ''

    with open(file_name, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

    csv_data_list = sorted(glob.glob("data/*.csv"))

    # Create an empty df (data frame) with the files' column names.
    df = pd.DataFrame()
    #Date format: Year-Month-Day
    date_format ='%Y-%m-%d'
    one_day = datetime.timedelta(days=1)

    # Go through the data and replace the df content each time a new file is accessed.
    for data in csv_data_list:
        #print(data)
        df = pd.read_csv(data)

        split_string = data.split("/",1)
        contract_exp = split_string[1]
        #print(contract_exp)

        parsed_contract_date = datetime.datetime.strptime(contract_exp, date_format)

        #IF LAST_DATE EMPTY <-- FIRST TRADE_DATE
        if last_date == '':
            # last_date = first file's first trade date
        else:
            parsed_last_date = parsed_last_date + one_day

        #COMPARE EXP_DATE WITH LAST_DATE

        #COMPARE EXP_DATE WITT EXP_DATE - ROLL_DAYS


        # df.loc[df['Trade Date'] >= '' & df['Trade Date'] <= '']


        # APPEND ALL ENTRIES UNTIL EXPIRATION MINUS ROLL_DAYS

        # ROLL TO THE NEXT CONTRACT AND OPEN NEXT FILE


    return

# TODO EDIT AFTER TESTING
# Execute
generate_time_series("2013-01-16", '0', '1')
