import sys
import glob, os
import heapq
import itertools

# This module should read in the parameters
# or ask for parameters to be entered.
# TODO

# function to read in a file into a dictionary
# this should also take in number of lines to read
# and return also that file has ended. 
class DataFile:

    def get_handle(file_location):
        in_file = open(file_location, "r")
        return in_file

    def read_file(file_handle, lines_to_read, offset):
        end_of_file = False
        file_dict = {}
        count = 0
        file_handle.seek(offset)
        while count < lines_to_read and not end_of_file: 
            line = file_handle.readline().strip()
            if line == '':
                end_of_file = True
                break
            (key, val) = line.split()
            file_dict[key] = int(val)
            count +=1

        offset = file_handle.tell()
        if end_of_file:
            file_handle.close()
        return (file_dict, offset, end_of_file)

# Function will sort a dict object to return a sorted dict
def sort_file(file_dict):
    print("sort file")
    sorted_dict = dict(sorted(file_dict.items(), key = lambda item: item[1], reverse=True))
    return sorted_dict


# this should also take in a file suffix like 'out', 1, 2, to append to file name written
def write_file(sorted_dict,suffix):
    print("write file")
    with open('outfile_{}.txt'.format(str(suffix)), 'w') as f:
        for key,value in sorted_dict.items():
            f.write("%s %s\n" % (key,value))


# Function to sort merge n-files.  This could use a priority queue 
def sort_merge_files():
    print("sort merge n-files")
    # read all outfile_# into separate dict
        # scan all files with 'outfile_' prefix
    out_directory = "./"
    os.chdir(out_directory)
    result = {}
    result_dict = {}
    for file in glob.glob("outfile_*.txt"):
        # read each of these files into a separate dict
        temp_dict = {}
        with open(file, 'r') as f:
            for line in f:
                key, val = line.split()
                temp_dict[key] = int(val)
        # use heapq.merge(iterables, key, reverse = True)  two dict at a time, this maybe better than doing an n-file merge sort in case
        # of limited storage.  The merged files can then be deleted as we pull more file segements from remote.
        # got stuck here as took me a while to figure out how to use dict with heapq.merge
        result_generator = heapq.merge(temp_dict.items(), result_dict.items(), key = lambda item:item[1], reverse=True)
        # Saving only the first 500 items in merge sorted dict
        sliced_generator = itertools.islice(result_generator, 500)
        result_dict = {c[0]:c[1] for c in sliced_generator}
        
    # write the result
    write_file(result_dict, "final")


DEFAULT_FILE_LOCATION = '/home/azhar/projects/triad-challenge/triad-challenge/spacemaps_technical_challenge.txt'

file_location = ''

# read in the file name from command line
# parameters must be X, location of file.   (these 2 are required)
# initially I can use local file later on I will change it to remote file. 
# main function will read command line parameters
def main():
    X = 10
    file_location = sys.argv[1] if len(sys.argv) >=2 else DEFAULT_FILE_LOCATION
    print(file_location)
    # get count of lines in file.. then calculate the number of lines per file read 
    # OR amount of lines you want to read at a time
    # create a loop that will keep calling read_file(), sort_file(), write_file() until 
    # end of file is reached.
    end_of_file = False
    offset = 0
    lines_to_read = 500
    file_handle = DataFile.get_handle(file_location)

    # skip the first 500 bytes
    file_dict, offset, end_of_file = DataFile.read_file(file_handle, 0, 500)
    file_suffix = 1
    while not end_of_file:
        file_dict, offset, end_of_file = DataFile.read_file(file_handle, lines_to_read, offset)
        sorted_dict = sort_file(file_dict)
        write_file(sorted_dict, file_suffix)
        file_suffix += 1
    
    # do n sort file merge
    # get the top X numbers from the final file
    sort_merge_files()


if __name__ == '__main__':
    main()