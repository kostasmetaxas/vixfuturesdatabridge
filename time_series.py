import pandas as pd
import numpy as np
import datetime
import glob
import csv
import sys
from vix_futures_exp_dates import run_over_time_frame

#Date format: Year-Month-Day
date_format ='%Y-%m-%d'



# USE THESE AS DEFAULTS IF NO ARGUMENTS
# first_target_contract = "2013-01-16"
#
# roll_days = 0
#
# forward = 1


# TODO LOCATE TARGET CONTRACT
# TODO IMPLEMENT SMOOTHING
# TODO WHEN APPENDING DATA TO TIME SERIES INCLUDE FILE NAME
#

# target_date: Time series' starting point. Input in '%Y-%m-%d' format.
# roll_days: Amount of days ,before current contract expiration, roll to the next contract.
# months_forward: Refers to the VX<forward>. Example: if forward=2 calculate VX2 curve.
def generate_time_series(target_date, roll_days, months_forward, smoothing):

    # Create new .csv file where time series data will be inserted.
    file_name = first_target_contract + '_' + roll_days + '_' + months_forward + '_Time_Series.csv'
    last_used_date = ''


    expiration_dates_list = run_over_time_frame()

    target_date_parsed = datetime.datetime.strptime(target_date, date_format)

    valid_contracts = 0


    '''
    Comparing the input date with each contract's expiration date.
    If the input date is past the contract's expiration +1 is added to the
    valid_contract counter. If valid_contract == forward the first target contract
    means we reached the desired month and are past the first_target_contract.
    To go back to the correct contract we subtract 1 from the index returned
    when the loop is broken.
    '''
    for target_contract_index, a_contract in enumerate(expiration_dates_list):

        a_contract_parsed = datetime.datetime.strptime(a_contract, date_format)

        if target_date_parsed >= a_contract_parsed:
            valid_contracts += 1

            if valid_contracts == months_forward:
                break

    first_target_contract = expiration_dates_list[target_contract_index - 1]

    with open(file_name, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)


    '''
    Creating a list with the available contracts and removing the ones not
    needed before the target contract so that the time series starts from the
    correct point in time.
    '''
    csv_data_list = sorted(glob.glob("data/*.csv"))
    try:
        target_index = csv_data_list.index(first_target_contract)
    except ValueError:
        sys.exit('Invalid target contract index.')

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



#---------------------------------------------------------------------------------------------------------------------------------------------



    # Go through the data and replace the df content each time a new file is accessed.
    for data in csv_data_list:
        #print(data)
        df = pd.read_csv(data)

        # KEEP LAST ENTRY
        split_string = data.split("/",1)
        contract_exp = split_string[1]
        #print(contract_exp)


        parsed_contract_date = datetime.datetime.strptime(contract_exp, date_format)


        #IF last_used_date EMPTY <-- FIRST TRADE_DATE
        if last_used_date == '':
            # last_used_date = first file's first trade date
        else:
            parsed_last_used_date = parsed_last_used_date + one_day


        if parsed_last_used_date == (parsed_contract_date - parsed_roll_days):
            #ROLL, USE NEXT FILE, START FROM PARSED_last_used_date TRADE_DATE
        else:
            df.loc[df['Trade Date'] >= '' & df['Trade Date'] <= '']
            #COPY ROW, TO FIND ROW COMPARE PARSED_last_used_date WITH TRADE_DATE IN CSV


        #COMPARE EXP_DATE WITH last_used_date

        #COMPARE EXP_DATE WITT EXP_DATE - ROLL_DAYS



        #REMOVE AFTER TEST
        print(df)
        break

    return

# TODO EDIT AFTER TESTING
# Execute
generate_time_series("2013-01-16", '0', '1', False)
