from MaxHeap import MaxHeap
import sys
import os
from tqdm import tqdm
from DataFile import DataFile
import time
import click
import validators
from pathlib import Path
import ProcessSortedMemoryMerges
import ProcessSinglePriorityQueue
import ProcessUsingLocalFileSortMerges

# This module reads in the command line parameters and 
# has the class and functions to execute the main process. 


class LargestValues:
    DEFAULT_X = 10
    DEFAULT_FILE_LOCATION = '/home/azhar/projects/triad-challenge/triad-challenge/spacemaps_technical_challenge_orig.txt'
    REMOTE_FILE_LOCATION = 'https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com/spacemaps_technical_challenge.txt'
    CHUNK_SIZE_IN_BLOCKS = 8 # each block is 1024 byte


    def processSortedMemoryMerges(url, chunk_size, offset_bytes, x_largest_values):
        sortedMemoryMerge = ProcessSortedMemoryMerges.SortedMemoryMerge()
        sortedMemoryMerge.process(url, int(chunk_size), offset_bytes, int(x_largest_values))


    def processSinglePriorityQueueMerges(url, chunk_size, offset_bytes, x_largest_values):
        singlePriorityQueueMerges = ProcessSinglePriorityQueue.SinglePriorityQueueMerges()
        singlePriorityQueueMerges.process_maxheap( url, chunk_size, offset_bytes, x_largest_values)


    def processUsingLocalFileMerges(file_name, x_largest_values):
        out_directory = 'out'
        localFileSortMerges = ProcessUsingLocalFileSortMerges.LocalFileSortMerges()
        localFileSortMerges.process_with_local_files( file_name, x_largest_values, out_directory)
    

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
    LargestValues.processSinglePriorityQueueMerges(url, int(chunk_size), offset_bytes, int(x))

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
    LargestValues.processUsingLocalFileMerges(file, int(x))



if __name__ == '__main__':
    cli()