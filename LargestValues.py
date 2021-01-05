from MaxHeap import MaxHeap
import sys
import glob, os
import heapq
import itertools
from tqdm import tqdm
import FileDownloader
from DataFile import DataFile
import time
import click
import validators
from pathlib import Path
import ProcessSortedMemoryMerges

# This module reads in the command line parameters and 
# has the class and functions to execute the main process. 




class LargestValues:
    DEFAULT_X = 10
    DEFAULT_FILE_LOCATION = '/home/azhar/projects/triad-challenge/triad-challenge/spacemaps_technical_challenge_orig.txt'
    REMOTE_FILE_LOCATION = 'https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com/spacemaps_technical_challenge.txt'
    CHUNK_SIZE_IN_BLOCKS = 8 # each block is 1024 byte

    file_location = ''
    result_dict = {}
    X_largest_values = 0
    max_heap = None


    def processSortedMemoryMerges(url, chunk_size, offset_bytes, x):
        sortedMemoryMerge = ProcessSortedMemoryMerges.SortedMemoryMerge
        sortedMemoryMerge.process(sortedMemoryMerge,url, int(chunk_size), offset_bytes, int(x))

    def process_maxheap(remote_file_url, chunk_size, offset_bytes, x_largest_values):
        LargestValues.max_heap = MaxHeap([],x_largest_values)
        response_handle = FileDownloader.get_response_handle(remote_file_url, offset_bytes)
        file_size = int(response_handle.headers.get('content-length', 0))
        LargestValues.progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)
        FileDownloader.get_chunks(response_handle, chunk_size, offset_bytes, LargestValues.process_single_maxheap)

    def process_single_maxheap(lines, last_chunk, chunk_size):
        LargestValues.progress_bar.update(chunk_size)
        for line in lines:
            key, value = line.split()
            LargestValues.max_heap.add((int(value),key))
        if last_chunk:
            LargestValues.progress_bar.close()
            # write the result
            elements = LargestValues.max_heap.getLargest()
            for elem in elements:
                print(elem[1],' ', elem[0])


    def process_with_local_files(file_location, X_largest_numbers):
        # Get count of lines in file.. then calculate the number of lines per file read 
        # OR amount of lines you want to read at a time <-- used this , ignore above
        # create a loop that will keep calling read_file(), sort_dict(), write_file() until 
        # end of file is reached.
        end_of_file = False
        offset = 0
        # process the local file 500 lines at a time
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


# Read in the file name from command line
# parameters must be X, location of file.   (these 2 are required)
# initially I can use local file later on I will change it to remote file. 
# main function will read command line parameters
def main(remote_file_url, x_largest_numbers,chunk_size_in_blocks):
    file_location = sys.argv[1] if len(sys.argv) >=2 else LargestValues.DEFAULT_FILE_LOCATION
    offset_bytes = 500
    LargestValues.process(remote_file_url, chunk_size_in_blocks, offset_bytes, x_largest_numbers)
    LargestValues.process_maxheap(remote_file_url, chunk_size_in_blocks, offset_bytes, x_largest_numbers)
    LargestValues.process_with_local_files(file_location, x_largest_numbers)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS, chain=True)
def cli():
    # App for get the x largest values from a key-value data source
    # python LargestValues.py memory_merges
    # python LargestValues.py single_priority_queue
    # python LargestValues.py files_on_disk
    pass

@cli.command()
@click.option('--url', default=LargestValues.REMOTE_FILE_LOCATION, type=click.STRING, help='URL location for the data file')
@click.option('--x', default=LargestValues.DEFAULT_X, type=click.INT, help='Number of Largest Values to get from data file')
@click.option('--chunk_size', default=LargestValues.CHUNK_SIZE_IN_BLOCKS, type=click.INT, help= 'Size of chunk to retrieve from remote file and process at a time in blocks of 1024 bytes.')
def memory_merges(url, x, chunk_size):
    if not validators.url(url):
        print("Entered url did not pass validation, please make sure it is correct.")
        return
    offset_bytes = 500
    LargestValues.processSortedMemoryMerges(url, int(chunk_size), offset_bytes, int(x))

@cli.command()
@click.option('--url', default=LargestValues.REMOTE_FILE_LOCATION, type=click.STRING, help='URL location for the data file')
@click.option('--x', default=LargestValues.DEFAULT_X, type=click.INT, help='Number of Largest Values to get from data file')
@click.option('--chunk_size', default=LargestValues.CHUNK_SIZE_IN_BLOCKS, type=click.INT, help= 'Size of chunk to retrieve from remote file and process at a time in blocks of 1024 bytes.')
def single_priority_queue(url, x, chunk_size):
    if not validators.url(url):
        print("Entered url did not pass validation, please make sure it is correct.")
        return
    offset_bytes = 500
    LargestValues.process_maxheap(url, int(chunk_size), offset_bytes, int(x))

@cli.command()
@click.option('--file', default=LargestValues.DEFAULT_FILE_LOCATION, type=click.STRING, help='File location for the data file')
@click.option('--x', default=LargestValues.DEFAULT_X, type=click.INT, help='Number of Largest Values to get from data file')
@click.option('--chunk_size', default=LargestValues.CHUNK_SIZE_IN_BLOCKS, type=click.INT, help= 'Size of chunk to retrieve from remote file and process at a time in blocks of 1024 bytes.')
def files_on_disk(file, x, chunk_size):
    print(file)
    if not os.path.isfile(file):
        print("File not found, please make sure it is correct.")
        return
    offset_bytes = 500
    LargestValues.process_with_local_files(file, int(x))



if __name__ == '__main__':
    cli()