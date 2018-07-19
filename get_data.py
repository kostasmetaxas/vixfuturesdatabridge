import csv
import pandas
import pandas_market_calendars as market_cal
from datetime import datetime

cboe_calendar = market_cal.calendar_utils.get_calendar('CME')

# TODO: CROSS REFERENCE FOR HOLIDAYS
# TODO: IF HOLIDAY FIX DATE (30 DAYS PRIOR TO THE PRECEDING TRADING DAY)

#Checks if input date is a wednesday in the third week of the month.
#Date format: Year-Month-Day
#Returns True - False
def is_third_friday_of_month(input_date, initial_week_num):
    parsed_current_date = datetime.strptime(input_date, '%Y-%m-%d')
    current_week_num = parsed_current_date.isocalendar()[1]
    return (current_week_num == initial_week_num + 2) and (parsed_current_date.weekday() == 4)

#Goes through the years
for year in range(2013, 2014):

    #Goes through the months
    for month in range(1,13):
        month = "%02d" % month
        start_date = str(year) + '-' + str(month) + '-' + '01'

        parsed_initial_date = datetime.strptime(start_date, '%Y-%m-%d')
        initial_week_num = parsed_initial_date.isocalendar()[1]

        #Goes through the days
        for day in range (1,32):
            new_string_part = "%02d" % (day)
            new_string_part = str(new_string_part)

            current_year, current_month, current_day = start_date.split('-')
            current_day = new_string_part

            current_date = '-'.join([current_year, current_month, current_day])

            if is_third_friday_of_month(current_date, initial_week_num):
                print(current_date)

                # TODO: CHECK IF HOLIDAY
                # TODO: FIX DATE IF HOLIDAY

                #download_link = 'https://markets.cboe.com/us/futures/market_statistics/historical_data/products/csv/VX/' + vix_expiration_date
                #   print(download_link)
                break;
