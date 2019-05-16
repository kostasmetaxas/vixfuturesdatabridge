import os
import pandas
# from vix_futures_exp_dates import run_over_time_frame

DATELESS_LINK = 'https://markets.cboe.com/us/futures/market_statistics/historical_data/products/csv/VX/'
destination_folder_path = './new_data'


# Checks if data destination folder exist
def destination_folder_check(path):
    print("Checking for destination folder...")
    try:
        os.mkdir(path)
    except OSError:
        print ("Directory" + path + " already exists. Proceeding...")
    else:
        print ("Successfully created the directory " + path)


def download_raw_data(futures_exp_dates):

    destination_folder_check(destination_folder_path)

    failed_download_counter = 0

    print('Downloading data...')
    for expiration_date in futures_exp_dates:

        csv_name = expiration_date + '.csv'

        try:
            data = pandas.read_csv(DATELESS_LINK + expiration_date)
            data.to_csv(index=False, path_or_buf=destination_folder_path + '/' + csv_name)
            print(csv_name + " Downloaded.")
        except:
            failed_download_counter += 1
            print(expiration_date)
            print('TIMES FAILED: ', failed_download_counter)
            pass

        if failed_download_counter > 5:
            break
