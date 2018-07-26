import csv
import pandas
import pandas_market_calendars as market_cal
import datetime



# cboe_calendar = market_cal.calendar_utils.get_calendar('CME')
# holidays = cboe_calendar.holidays()



# TODO: CROSS REFERENCE FOR HOLIDAYS
# TODO: IF HOLIDAY FIX DATE (30 DAYS PRIOR TO THE PRECEDING TRADING DAY)

#Checks if input date is a wednesday in the third week of the month.
#Date format: Year-Month-Day
#Returns True - False
def is_third_friday_of_month(input_date, friday_counter):
    parsed_current_date = datetime.datetime.strptime(input_date, '%Y-%m-%d')
    current_week_num = parsed_current_date.isocalendar()[1]
    return (friday_counter == 3) and (parsed_current_date.weekday() == 4)



# TODO: fix years range

def run_over_time_frame():
    #Goes through the years

    for year in range(2018, 2019):

        #Goes through the months
        for month in range(1,13):
            month = "%02d" % month
            start_date = str(year) + '-' + str(month) + '-' + '01'

            parsed_initial_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            friday_counter = 0

            #Goes through the days
            for day in range (1,32):
                new_string_part = "%02d" % (day)
                new_string_part = str(new_string_part)

                current_year, current_month, current_day = start_date.split('-')
                current_day = new_string_part

                current_date = '-'.join([current_year, current_month, current_day])
                parsed_current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')

                if parsed_current_date.weekday() == 4:
                    friday_counter += 1

                if is_third_friday_of_month(current_date, friday_counter):
                    thirty_days = datetime.timedelta(days=30)
                    current_date_minus_month = parsed_current_date - thirty_days

                    if current_date_minus_month.weekday()==2:
                        print('VIX EXPIRATION', current_date_minus_month)

                    # TODO: CHECK IF HOLIDAY
                    # TODO: FIX DATE IF HOLIDAY

                    break;



#download_link = 'https://markets.cboe.com/us/futures/market_statistics/historical_data/products/csv/VX/' + vix_expiration_date
#   print(download_link)


# Execute
run_over_time_frame()
