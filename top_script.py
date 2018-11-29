from vix_futures_exp_dates import run_over_time_frame
from download_link import download_data
from time_series import generate_time_series
from compare_files import compare_files


def update_data():
    contract_expiration_list = run_over_time_frame()
    download_data(contract_expiration_list)
    compare_files()


def time_series_calls():
    contract_expiration_list = run_over_time_frame()
    generate_time_series("2014-05-27", 5, 1, True, contract_expiration_list)
    generate_time_series("2014-05-27", 5, 2, True, contract_expiration_list)
    generate_time_series("2014-05-27", 5, 3, True, contract_expiration_list)
    generate_time_series("2014-05-27", 5, 4, True, contract_expiration_list)
    generate_time_series("2014-05-27", 5, 5, True, contract_expiration_list)
    generate_time_series("2014-05-27", 5, 6, True, contract_expiration_list)


#Excecute
#update_data()
time_series_calls()
