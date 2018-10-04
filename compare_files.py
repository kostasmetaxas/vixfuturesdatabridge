import hashlib
import glob
import time

def hash_file(filename):

    # make a hash object
    hash = hashlib.sha1()

    with open(filename,'rb') as file:
        # loop until end of file
        chunk = 0
        while chunk != b'':
            #read only 1024 bytes at a timedelta
            chunk = file.read(1024)
            hash.update(chunk)

        # return hex of digest
        return hash.hexdigest()

print(hash_file("data/2013-01-16.csv"))
# hash_file("data/2013-01-16(copy).csv")

# ------------------------------------------------------------------------------

# def replace_file(file1,file2):


def compare_files():

    # current_data_list refers to the data that was used for the last calculation.
    current_data_list = sorted(glob.glob("data/*.csv"))
    # new_data_list refers to the most recently downloaded data
    new_data_list = sorted(glob.glob("new_data/*.csv"))


    #removing the "data/" and the "new_data/" parts.
    for index, a_file in enumerate(current_data_list):
        split_string = a_file.split("/",1)
        current_data_list[index] = split_string[1]

    for index, a_file in enumerate(new_data_list):
        split_string = a_file.split("/",1)
        new_data_list[index] = split_string[1]

# TODO COMPARE FILES WITH SAME NAME, HASH AND REPLACE IF NEEDED (FROM NEW_DATA TO DATA)






compare_files()
