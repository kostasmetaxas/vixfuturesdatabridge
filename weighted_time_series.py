import pandas as pd
import numpy as np
import datetime
import glob
import csv
import sys
from QuantLib import Business252
from download_link import folder_check

# from time_series import contract_finder


'''
Comparing the input date with each contract's expiration date.
If the input date is past the contract's expiration +1 is added to the
valid_contract counter. If valid_contract == forward the first target contract
means we reached the desired month and are past the first_target_contract.
Returns the first contract to be used in the time series.
'''
def contract_finder(target_date, expiration_dates_list, months_forward):
    valid_contracts = 0
    for target_contract_index, a_contract in enumerate(expiration_dates_list):

        if  a_contract >= target_date:
            valid_contracts += 1
            print("VALID CONTRACTS " + str(valid_contracts))

            if valid_contracts == months_forward:
                break
    first_target_contract = expiration_dates_list[target_contract_index]

    return first_target_contract


def business_days_until_expiration(current_date, expiration_date):

    # Business_instance = Business252();
    # serial_days = Business_instance.dayCount(current_date, expiration_date)

    # sliced_df = dataframe.loc[date_str:]
    # row_amount = len(sliced_df.index) + 1


    serial_days = pd.bdate_range(current_date, expiration_date)
    # print(serial_days.argmax())
    amount_of_days = serial_days.argmax()
    return amount_of_days





# target_date:      Time series' starting point. Input in '%Y-%m-%d' format.
# desired:          Amount of maturity days.
# months_forward:   <months_forward>m1m
def constant_maturity_time_series(target_date, desired, months_forward, expiration_dates_list):

    #Date format: Year-Month-Day
    date_format ='%Y-%m-%d'

    data_path = "./Results"
    folder_check(data_path)

    # Create new .json file where time series data will be inserted.
    file_name = data_path + '/' + target_date + '_' + str(desired) + '_' + str(months_forward) + '_Constant_Maturity.json'

    first_target_contract = contract_finder(target_date, expiration_dates_list, months_forward)


    '''
    Creating a list with the available contracts, sorted by expiration date
    and setting the index after the ones not needed before the target contract
    so that the time series starts from the correct point in time.
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
    next_df = pd.DataFrame()
    one_day = datetime.timedelta(days=1)
    thirty_days = datetime.timedelta(days=30)

    output_time_series = pd.DataFrame()
    parsed_last_used_date = ''
    # Goes through the file list and replaces the dataframe content each time a new file is accessed.
    counter = target_index

    while counter <= len(csv_data_list)-1:
        csv_file = csv_data_list[counter]
        df = pd.read_csv(csv_file)

        split_string = csv_file.split("/",1)
        temp_name_list1 = split_string[1]
        temp_name_list2 = temp_name_list1.split('.',1)
        expiration_date = temp_name_list2[0]
        # print(expiration_date)

        roll = False

        while not roll:
            try:
                parsed_expiration_date_current = datetime.datetime.strptime(expiration_date, date_format)
            except ValueError:
                sys.exit("Can't parse date.")

            if parsed_last_used_date == '':
                try:
                    parsed_last_used_date = datetime.datetime.strptime(target_date, date_format)
                except ValueError:
                    sys.exit("Can not parse date.")

            else:
                parsed_last_used_date = parsed_last_used_date + one_day

            date_indexed_df = df.set_index("Trade Date")

            # Emptying series so that previous data does not affect outcome.
            row = pd.Series([])
            next_row = pd.Series([])

            last_used_date_str = parsed_last_used_date.strftime(date_format)

            business_days_left = business_days_until_expiration(parsed_last_used_date, parsed_expiration_date_current)


            try:
                row = date_indexed_df.loc[last_used_date_str]
            except KeyError:
                pass

            try:
                # GET VALUES FROM THIS CONTRACT'S CURRENT DATE
                current_contract_open = row.loc["Open"]
                current_contract_high = row.loc["High"]
                current_contract_low = row.loc["Low"]
                current_contract_settle = row.loc["Settle"]
                current_contract_volume = row.loc["Total Volume"]
                current_contract_open_interest = row.loc["Open Interest"]

                # GET VALUES FROM NEXT CONTRACT'S SAME DATE
                next_csv_file = csv_data_list[counter+1]
                next_df = pd.read_csv(next_csv_file)
                next_date_indexed_df = next_df.set_index("Trade Date")
                next_row = next_date_indexed_df.loc[last_used_date_str]


                next_contract_open = next_row.loc["Open"]
                next_contract_high = next_row.loc["High"]
                next_contract_low = next_row.loc["Low"]
                next_contract_settle = next_row.loc["Settle"]
                next_contract_volume = next_row.loc["Total Volume"]
                next_contract_open_interest = next_row.loc["Open Interest"]



                split_string = next_csv_file.split("/",1)
                temp_name_list1 = split_string[1]
                temp_name_list2 = temp_name_list1.split('.',1)
                expiration_date_next = temp_name_list2[0]

                try:
                    parsed_expiration_date_next = datetime.datetime.strptime(expiration_date_next, date_format)
                except ValueError:
                    sys.exit("Can't parse date.")




                business_days_left_next = business_days_until_expiration(parsed_last_used_date, parsed_expiration_date_next)

                divisor = business_days_left - business_days_left_next
                print(divisor)

                if divisor == 0:
                    print("----DIVISOR ZERO ON------> " + last_used_date_str)
                else:
                    current_contract_weight = (desired - business_days_left_next) / divisor
                    next_contract_weight = 1 - current_contract_weight

                    #print("CURRENT WEIGHT --> " + str(current_contract_weight) + "     NEXT CONTRACT WEIGHT --> " + str(next_contract_weight))

                    new_open = (current_contract_open * current_contract_weight) + (next_contract_open * next_contract_weight)
                    new_high = (current_contract_high * current_contract_weight) + (next_contract_high * next_contract_weight)
                    new_low = (current_contract_low * current_contract_weight) + (next_contract_low * next_contract_weight)
                    new_settle = (current_contract_settle * current_contract_weight) + (next_contract_settle * next_contract_weight)
                    new_volume = (current_contract_volume * current_contract_weight) + (next_contract_volume * next_contract_weight)
                    new_open_interest = (current_contract_open_interest * current_contract_weight) + (next_contract_open_interest * next_contract_weight)

                    # SET ROW'S SETTLE TO NEW VALUE
                    row = row.replace({current_contract_settle : new_settle})

                    # APPEND ROW
                    output_time_series = output_time_series.append(row)

                # CONTINUE
            except KeyError:
                # print(last_used_date_str + " IS NOT A BUSINESS DAY")
                pass

            if parsed_last_used_date == parsed_expiration_date_current:
                print("-----------ROLLING--------------")
                roll = True


        counter += 1
    print(output_time_series)
    output_time_series.to_json(file_name, index=True)
