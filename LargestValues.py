import sys
import glob, os
import heapq
import itertools
from tqdm import tqdm
import FileDownloader
from DataFile import DataFile
import time
import click

# This module reads in the command line parameters and 
# has the class and functions to execute the main process. 

# Function to convert a line iterable into a dict
def dict_lines(lines):
    dict_segment = {}
    for line in lines:
        key, val = line.split()
        dict_segment[key] = int(val)
    return dict_segment


# Function will sort a dict object to return a sorted dict
def sort_dict(file_dict):
    # print("sort dict")
    sorted_dict = dict(sorted(file_dict.items(), key = lambda item: item[1], reverse=True))
    return sorted_dict


# Function to sort merge n files but 2 files at a time. 
# Can do n file merge as heapq.merge can take more than 2 iterables
# but in case of limited RAM and very large X value merging 2 files is better. 
def sort_merge_files(X_largest_numbers):
    print("sort merge files 2 at a time")
    # read all outfile_# into separate dict
        # scan all files with 'outfile_' prefix 
        # not a good design, needs to be refactored.
    out_directory = "./"
    os.chdir(out_directory)
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
        # Saving only the first X_largest_numbers items in merge sorted dict
        sliced_generator = itertools.islice(result_generator, X_largest_numbers)
        result_dict = {c[0]:c[1] for c in sliced_generator}
        
    # write the result_dict dictionary
    DataFile.write_file(result_dict, "result_final")

class LargestValues:
    DEFAULT_X = 10
    DEFAULT_FILE_LOCATION = '/home/azhar/projects/triad-challenge/triad-challenge/spacemaps_technical_challenge_orig.txt'
    REMOTE_FILE_LOCATION = 'https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com/spacemaps_technical_challenge.txt'

    file_location = ''
    progress_bar = None
    result_dict = {}
    X_largest_values = 0

    # this process can later be changed to call a different algorithm
    def process(remote_file_url, chunk_size, offset_bytes, X_largest_values):
        response_handle = FileDownloader.get_response_handle(remote_file_url, offset_bytes)        
        LargestValues.X_largest_values = X_largest_values
        LargestValues.get_chunks(response_handle, chunk_size, offset_bytes)

    def get_chunks(response_handle, chunk_size, offset_bytes):
        file_size = int(response_handle.headers.get('content-length', 0))
        LargestValues.progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)
        FileDownloader.get_chunks(response_handle, chunk_size, offset_bytes, LargestValues.process_chunk)

    def process_chunk(lines, last_chunk, chunk_size):
        LargestValues.progress_bar.update(chunk_size)
        dict_chunk = dict_lines(lines)
        sorted_dict_chunk = sort_dict(dict_chunk)
        result_generator = heapq.merge(sorted_dict_chunk.items(), LargestValues.result_dict.items(),
            key = lambda item:item[1], reverse=True)
        # Saving only the first X items in merge sorted dict
        sliced_generator = itertools.islice(result_generator, LargestValues.X_largest_values)
        LargestValues.result_dict = {c[0]:c[1] for c in sliced_generator}
        # time.sleep(1)
        if last_chunk:
            # write the result
            DataFile.write_file(LargestValues.result_dict, "result_final")
            LargestValues.progress_bar.close()
            for k, v in LargestValues.result_dict.items():
                print(k)
                
    def processWithLocalFiles(file_location, X_largest_numbers):
        # get count of lines in file.. then calculate the number of lines per file read 
        # OR amount of lines you want to read at a time
        # create a loop that will keep calling read_file(), sort_dict(), write_file() until 
        # end of file is reached.
        end_of_file = False
        offset = 0
        lines_to_read = 500
        file_handle = DataFile.get_handle(file_location)

        # skip the first 500 bytes
        file_dict, offset, end_of_file = DataFile.read_file(file_handle, 0, 500)
        # Write the read file into sorted segmented file chunks
        file_suffix = 1
        # here this writes the same file_name prefix as to be read by sort_merge_files 
        # not a good design, needs to be refactored. 
        file_name_prefix = "outfile_"
        while not end_of_file:
            file_dict, offset, end_of_file = DataFile.read_file(file_handle, lines_to_read, offset)
            sorted_dict = sort_dict(file_dict)
            DataFile.write_file(sorted_dict, file_name_prefix + str(file_suffix))
            file_suffix += 1

        # do n sort file merge
        # get the top X numbers from the final file
        sort_merge_files(X_largest_numbers)

    

# Read in the file name from command line
# parameters must be X, location of file.   (these 2 are required)
# initially I can use local file later on I will change it to remote file. 
# main function will read command line parameters
def main(remote_file_url, x_largest_numbers):
    file_location = sys.argv[1] if len(sys.argv) >=2 else LargestValues.DEFAULT_FILE_LOCATION
    offset_bytes = 500
    chunk_size_in_blocks = 8 # each block is 1024 byte

    LargestValues.process(remote_file_url, chunk_size_in_blocks, offset_bytes, x_largest_numbers)
    #LargestValues.processWithLocalFiles(file_location, X_largest_numbers)

@click.command()
@click.option('--url', default=LargestValues.REMOTE_FILE_LOCATION, help='URL location for the data file')
@click.option('--x', default=LargestValues.DEFAULT_X, help='Number of Largest Values to get from data file')
def cli(url, x):
    main(url, int(x))


if __name__ == '__main__':
    cli()