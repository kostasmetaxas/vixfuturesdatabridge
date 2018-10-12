import pandas as pd
import numpy as np
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
def VIX_time_series(first_target_contract, roll_days, forward):

    # TODO DEFAULT VALUES IF EMPTY PARAMS

    # Create new .csv file. Time series data will be inserted.
    file_name = 'VX' + forward + '_Time_Series.csv'

    with open(file_name, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)


    # OPEN FIRST TARGET CONTRACT FILE

    # REPEAT UNTIL THERE IS NO NEXT FILE TO USE

        # APPEND ALL ENTRIES UNTIL EXPIRATION MINUS ROLL_DAYS

        # ROLL TO THE NEXT CONTRACT AND OPEN NEXT FILE


    return

# TODO EDIT AFTER TESTING
# Execute
VIX_time_series("2013-01-16", '0', '1')
