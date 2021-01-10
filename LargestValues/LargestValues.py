import os
from DataFile import DataFile
import time
import click
import validators
from pathlib import Path
import ProcessSortedMemoryMerges
import ProcessSinglePriorityQueue
import ProcessUsingLocalFileSortDiskMerge
#import ProcessUsingLocalFileSortMerges
import ProcessSortedNWayInMemoryMerge


# This module reads in the command line parameters and 
# has the class and functions to execute the main process. 


class LargestValues:
    DEFAULT_X = 10
    DEFAULT_FILE_LOCATION = './test_data/spacemaps_technical_challenge_orig.txt'
    REMOTE_FILE_LOCATION = 'https://amp-spacemaps-technical-challenge.s3-ap-northeast-1.amazonaws.com/spacemaps_technical_challenge.txt'
    CHUNK_SIZE_IN_BLOCKS = 8 # each block is 1024 byte
    DEFAULT_OUT_DIRECTORY = 'out'
    DEFAULT_OFFSET_BYTES = 500

    def __init__(self):
        self.test = ''

    # Following can be simplified / refactored with a Command pattern
    def processSortedMemoryMerges(url, chunk_size, offset_bytes, x_largest_values):
        sortedMemoryMerge = ProcessSortedMemoryMerges.SortedMemoryMerge()
        sortedMemoryMerge.process(url, int(chunk_size), offset_bytes, int(x_largest_values))


    def processSinglePriorityQueueMerges(url, chunk_size, offset_bytes, x_largest_values):
        singlePriorityQueueMerges = ProcessSinglePriorityQueue.SinglePriorityQueueMerges()
        singlePriorityQueueMerges.process( url, chunk_size, offset_bytes, x_largest_values)


    def processSortedMemoryNWayMerges(url, chunk_size, offset_bytes, x_largest_values):
        sortedMemoryNWayMerges = ProcessSortedNWayInMemoryMerge.SortedNWayMemoryMerge()
        sortedMemoryNWayMerges.process( url, int(chunk_size), offset_bytes, int(x_largest_values))
    
    def processUsingLocalFileDiskMerges(self, x_largest_values, chunk_size, offset_bytes, url):
        localFileSortDiskMerges = ProcessUsingLocalFileSortDiskMerge.LocalFileSortDiskMerge()
        #localFileSortDiskMerges.test_process_using_local_file(file_name,x_largest_values, self.DEFAULT_OUT_DIRECTORY)
        localFileSortDiskMerges.process(url, chunk_size, offset_bytes, x_largest_values,self.DEFAULT_OUT_DIRECTORY)

# Read in the file name from command line
# parameters must be X, location of file.   (these 2 are required)
# initially I can use local file later on I will change it to remote file. 
# main function will read command line parameters
# def main(remote_file_url, x_largest_numbers,chunk_size_in_blocks):
#     file_location = sys.argv[1] if len(sys.argv) >=2 else LargestValues.DEFAULT_FILE_LOCATION
#     offset_bytes = 500
#     LargestValues.process(remote_file_url, chunk_size_in_blocks, offset_bytes, x_largest_numbers)
#     LargestValues.process_maxheap(remote_file_url, chunk_size_in_blocks, offset_bytes, x_largest_numbers)
#     LargestValues.process_with_local_files(file_location, x_largest_numbers)

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
@click.option('--offset_bytes', default= LargestValues.DEFAULT_OFFSET_BYTES, type=click.INT, help = 'Bytes to skip in start of input file')
def memory_merges(url, x, chunk_size, offset_bytes):
    if not validators.url(url):
        print("Entered url did not pass validation, please make sure it is correct.")
        return
    offset_bytes = 500
    LargestValues.processSortedMemoryMerges(url, int(chunk_size), offset_bytes, int(x))

@cli.command()
@click.option('--url', default=LargestValues.REMOTE_FILE_LOCATION, type=click.STRING, help='URL location for the data file')
@click.option('--x', default=LargestValues.DEFAULT_X, type=click.INT, help='Number of Largest Values to get from data file')
@click.option('--chunk_size', default=LargestValues.CHUNK_SIZE_IN_BLOCKS, type=click.INT, help= 'Size of chunk to retrieve from remote file and process at a time in blocks of 1024 bytes.')
@click.option('--offset_bytes', default= LargestValues.DEFAULT_OFFSET_BYTES, type=click.INT, help = 'Bytes to skip in start of input file')
def single_priority_queue(url, x, chunk_size, offset_bytes):
    if not validators.url(url):
        print("Entered url did not pass validation, please make sure it is correct.")
        return
    LargestValues.processSinglePriorityQueueMerges(url, int(chunk_size), offset_bytes, int(x))

@cli.command()
@click.option('--url', default=LargestValues.REMOTE_FILE_LOCATION, type=click.STRING, help='URL location for the data file')
@click.option('--x', default=LargestValues.DEFAULT_X, type=click.INT, help='Number of Largest Values to get from data file')
@click.option('--chunk_size', default=LargestValues.CHUNK_SIZE_IN_BLOCKS, type=click.INT, help= 'Size of chunk to retrieve from remote file and process at a time in blocks of 1024 bytes.')
@click.option('--offset_bytes', default= LargestValues.DEFAULT_OFFSET_BYTES, type=click.INT, help = 'Bytes to skip in start of input file')
def nway_memory_merges(url, x, chunk_size, offset_bytes):
    if not validators.url(url):
        print("Entered url did not pass validation, please make sure it is correct.")
        return
    LargestValues.processSortedMemoryNWayMerges(url, int(chunk_size), offset_bytes, int(x))

@cli.command()
@click.option('--url', default=LargestValues.REMOTE_FILE_LOCATION, type=click.STRING, help='URL location for the data file')
#@click.option('--file', default=LargestValues.DEFAULT_FILE_LOCATION, type=click.STRING, help='File location for the data file')
@click.option('--x', default=LargestValues.DEFAULT_X, type=click.INT, help='Number of Largest Values to get from data file')
@click.option('--chunk_size', default=LargestValues.CHUNK_SIZE_IN_BLOCKS, type=click.INT, help= 'Size of chunk to retrieve from remote file and process at a time in blocks of 1024 bytes.')
@click.option('--offset_bytes', default= LargestValues.DEFAULT_OFFSET_BYTES, type=click.INT, help = 'Bytes to skip in start of input file')
def files_on_disk_merge( x, chunk_size, url, offset_bytes):
    if not validators.url(url):
        print("Entered url did not pass validation, please make sure it is correct.")
        return
    print('Using URL: ', url)
    print('Using X-largest-values: ', x)
    print('Using Chunk size in Blocks of 1024 bytes: ', chunk_size)
    LargestValues.processUsingLocalFileDiskMerges(LargestValues, int(x), chunk_size, offset_bytes, url)


if __name__ == '__main__':
    cli()