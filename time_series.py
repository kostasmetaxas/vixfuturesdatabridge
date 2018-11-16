import pandas as pd
import numpy as np
import datetime
import glob
import csv
import sys
from vix_futures_exp_dates import run_over_time_frame



# target_date:      Time series' starting point. Input in '%Y-%m-%d' format.
# roll_days:        Amount of days ,before current contract expiration, roll to the next contract.
# months_forward:   Refers to the VX<forward>. Example: if forward=2 calculate VX2 curve.
# smoothing :       Toggle time-series smoothing starting on roll date using the perpetual series method.
def generate_time_series(target_date, roll_days, months_forward, smoothing):

    #Date format: Year-Month-Day
    date_format ='%Y-%m-%d'

    if roll_days > 15:
        sys.exit('Maximum roll days 15. Insert valid amount of days')


    # Create new .csv file where time series data will be inserted.
    file_name = target_date + '_' + str(roll_days) + '_' + str(months_forward) + '_Time_Series.csv'

    expiration_dates_list = run_over_time_frame()
    valid_contracts = 0


    '''
    Comparing the input date with each contract's expiration date.
    If the input date is past the contract's expiration +1 is added to the
    valid_contract counter. If valid_contract == forward the first target contract
    means we reached the desired month and are past the first_target_contract.
    '''
    for target_contract_index, a_contract in enumerate(expiration_dates_list):

        if  a_contract >= target_date:
            valid_contracts += 1
            print("VALID CONTRACTS " + str(valid_contracts))

            if valid_contracts == months_forward:
                break

    # TODO
    # FIX target_contract_index SO THAT IT NEVER LANDS OFF THE LIST
    print("TARGET INDEX " + str(target_contract_index))
    first_target_contract = expiration_dates_list[target_contract_index]

    with open(file_name, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)


    '''
    Creating a list with the available contracts and removing the ones not
    needed before the target contract so that the time series starts from the
    correct point in time.
    '''
    csv_data_list = sorted(glob.glob("data/*.csv"))
    date_list = []

    for index, a_file in enumerate(csv_data_list):
        temp_split_string = a_file.split('/',1)
        split_string = temp_split_string[1].split('.',1)
        date_list.append(split_string[0])

    try:
        target_index = date_list.index(first_target_contract)
    except ValueError:
        sys.exit('Invalid target contract index.')




    # Create an empty df (data frame) with the files' column names.
    df = pd.DataFrame()
    #Date format: Year-Month-Day
    date_format ='%Y-%m-%d'
    one_day = datetime.timedelta(days=1)
    parsed_roll_days = datetime.timedelta(days=roll_days)



#-------------------------------------------------------------------------------------------------------------------------------------------

# TODO IMPLEMENT SMOOTHING
# TODO WHEN APPENDING DATA TO TIME SERIES INCLUDE FILE NAME

    # Amount of weight shifted from the current contract to the next during rolls.
    if roll_days > 0:
        shift_weight = 100 / roll_days

    output_time_series = pd.DataFrame()
    parsed_last_used_date = ''
    # Goes through the file list and replaces the dataframe content each time a new file is accessed.
    counter = target_index
    while counter <= len(csv_data_list):

        csv_file = csv_data_list[counter]
        df = pd.read_csv(csv_file)
        # print(df)

        # KEEP LAST ENTRY

        split_string = csv_file.split("/",1)
        temp_name_list1 = split_string[1]
        temp_name_list2 = temp_name_list1.split('.',1)
        expiration_date = temp_name_list2[0]
        # print(expiration_date)

        current_contract_weight = 100
        next_contract_weight    = 0

        roll = False

        while not roll:
            try:
                parsed_expiration_date = datetime.datetime.strptime(expiration_date, date_format)
            except ValueError:
                sys.exit("Can't parse date.")

            parsed_roll_date = parsed_expiration_date - parsed_roll_days

            if parsed_last_used_date == '':
                try:
                    parsed_last_used_date = datetime.datetime.strptime(target_date, date_format)
                except ValueError:
                    sys.exit("Can not parse date.")

            else:
                parsed_last_used_date = parsed_last_used_date + one_day


            date_indexed_df = df.set_index("Trade Date")

            last_used_date_str = parsed_last_used_date.strftime(date_format)

            try:
                row = date_indexed_df.loc[last_used_date_str]
                output_time_series = output_time_series.append(row)
            except KeyError:
                sys.exit("Item not found in DataFrame")

            print(output_time_series)


            #COPY ROW, TO FIND ROW COMPARE PARSED_last_used_date WITH TRADE_DATE IN CSV

            # CHECK IF SMOOTHING
            # if smoothing:
                # TRUE, GET ROW FROM NEXT FILE AND SMOOTH

            # APPEND ROW IN TIME SERIES FILE

            if smoothing and parsed_last_used_date > parsed_roll_date:
                # TODO IMPLEMENT SMOOTHING ON SETTLE VALUES
                current_contract_weight -= shift_weight
                next_contract_weight    += shift_weight


            else:
                if parsed_last_used_date == (parsed_roll_date):
                    roll = True
                else:
                    print()

        counter += 1


    # return output_time_series

# TODO EDIT AFTER TESTING
# Execute
generate_time_series("2014-05-27", 0, 1, False)
