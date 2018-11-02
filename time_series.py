import pandas as pd
import numpy as np
import datetime
import glob
import csv
import sys

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
# months_forward: Refers to the VX<forward>. Example: if forward=2 calculate VX2 curve.
def generate_time_series(first_target_contract, roll_days, months_forward):


    # Create new .csv file where time series data will be inserted.
    file_name = first_target_contract + '_' + roll_days + '_' + months_forward + '_Time_Series.csv'
    last_date = ''


    with open(file_name, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

    csv_data_list = sorted(glob.glob("data/*.csv"))
    #DELETE ALL ENTRIES UP TO first_target_contract
    try:
        target_index = csv_data_list.index(first_target_contract)
    except ValueError:
        sys.exit('Invalid target contract expiration date.')


    #Removing contracts before the first target contract so that the time series does not contain previous data.
    while True:
        split_string = csv_data_list[0].split("/",1)
        if split_string != first_target_contract:
            csv_data_list.remove(0)
        else:
            break


    # Create an empty df (data frame) with the files' column names.
    df = pd.DataFrame()
    #Date format: Year-Month-Day
    date_format ='%Y-%m-%d'
    one_day = datetime.timedelta(days=1)
    parsed_roll_days = datetime.timedelta(days = roll_days)


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


        if parsed_last_date == (parsed_contract_date - parsed_roll_days):
            #ROLL, USE NEXT FILE, START FROM PARSED_LAST_DATE TRADE_DATE
        else:
            df.loc[df['Trade Date'] >= '' & df['Trade Date'] <= '']
            #COPY ROW, TO FIND ROW COMPARE PARSED_LAST_DATE WITH TRADE_DATE IN CSV


        #COMPARE EXP_DATE WITH LAST_DATE

        #COMPARE EXP_DATE WITT EXP_DATE - ROLL_DAYS



        #REMOVE AFTER TEST
        print(df)
        break

    return

# TODO EDIT AFTER TESTING
# Execute
generate_time_series("2013-01-16", '0', '1')
