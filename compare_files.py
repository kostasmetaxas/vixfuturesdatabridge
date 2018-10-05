import hashlib
import glob
import time
from os.path import exists
from shutil import copyfile, copy

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


# ------------------------------------------------------------------------------

# def replace_file(file1,file2):


def compare_files():

    # current_data_list refers to the data that was used for the last calculation.
    current_data_list = sorted(glob.glob("data/*.csv"))
    # new_data_list refers to the most recently downloaded data.
    new_data_list = sorted(glob.glob("new_data/*.csv"))


    #removing the "data/" and the "new_data/" parts.
    for index, a_file in enumerate(current_data_list):
        split_string = a_file.split("/",1)
        current_data_list[index] = split_string[1]

    for index, a_file in enumerate(new_data_list):
        split_string = a_file.split("/",1)
        new_data_list[index] = split_string[1]

# TODO COMPARE FILES WITH SAME NAME, HASH AND REPLACE IF NEEDED (FROM NEW_DATA TO DATA)


    for index, a_file in enumerate(new_data_list):
        try:
            # Only compares file names. Not content.
            if a_file == current_data_list[index]:
                # Using hash to compare content.
                current_file_hash = hash_file("data/" + a_file)
                new_file_hash = hash_file("new_data/" + a_file)
                if current_file_hash != new_file_hash:
                    # Overwrites old version with the updated one.
                    copyfile("new_data/" + a_file, "data/" + a_file)
                    print("REPLACE")
        except IndexError:
            # Refers to new files in new_data_list that do not exist in current_data_list.
            print("EXTRA FILE")
            copy("new_data/" + a_file, "data/")
            pass
        except FileNotFoundError:
            # Refers to the files in the current_data_list. It is impossible to occur in new_data_list as a for-each loop is implemented.
            print("FILE TO BE HASHED, NOT FOUND")
            pass



# Excecute
compare_files()
