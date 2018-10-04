import hashlib
import glob

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

def compare_files(file1,file2):
    
def replace_file(file1,file2):
    
    
    # current_data_list refers to the data that was used for the last calculation.
    current_data_list = glob.glob("data/*.csv")
    # new_data_list refers to the most recently downloaded data
    new_data_list = glob.glob("new_data/*.csv")

    print(current_data_list[0] +" "+ new_data_list[0])
