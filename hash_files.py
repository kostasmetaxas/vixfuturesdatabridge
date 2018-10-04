import hashlib

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
