import heapq
import itertools
from DataFile import DataFile
import os, glob, shutil
import DictHelper

class LocalFileSortMerges:

    
    directory_name = ''

    # def __init__(self):
    #     self.x_largest_values = 0    

    # Function to sort merge n files but 2 files at a time. 
    # Can do n file merge as heapq.merge can take more than 2 iterables
    # but in case of limited RAM and very large X value merging 2 files is better. 
    def sort_merge_files(self, x_largest_numbers):
        print("sort merge files 2 at a time")
        # read all outfile_# into separate dict
            # scan all files with 'outfile_' prefix 
            # not a good design, needs to be refactored.
        # os.chdir(self.directory_name)
        result_dict = {}
        for file in glob.glob("outfile_*.txt"):
            # read each of these files into a separate dict
            temp_dict = {}
            with open(file, 'r') as f:
                for line in f:
                    key, val = line.split()
                    temp_dict[key] = int(val)
            # use heapq.merge(iterables, key, reverse = True)  two dict at a time, this maybe better than doing an n-file merge sort in case
            # of memory space.  The merged files can then be deleted as we pull more file segements from remote.
            # got stuck here as took me a while to figure out how to use dict with heapq.merge
            result_generator = heapq.merge(temp_dict.items(), result_dict.items(), key = lambda item:item[1], reverse=True)
            # Saving only the first X_largest_numbers items in merge sorted dict
            sliced_generator = itertools.islice(result_generator, x_largest_numbers)
            result_dict = {c[0]:c[1] for c in sliced_generator}

        # write the result_dict dictionary
        result_file = "result_final"
        #DataFile.write_file(result_dict, result_file)
        for k,v in result_dict.items():
            print(k)



        

    def process(self,file_location, x_largest_numbers, destination_dir):
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
        self.directory_name = destination_dir
        if self.directory_name:
            dir = 'out'
            if os.path.exists(dir):
                shutil.rmtree(dir)
                os.makedirs(dir)
            else:
                os.makedirs(dir)

        os.chdir(self.directory_name)
        file_name_prefix = "outfile_"
        while not end_of_file:
            file_dict, offset, end_of_file = DataFile.read_file(file_handle, lines_to_read, offset)
            sorted_dict = DictHelper.sort_dict(file_dict)
            DataFile.write_file(sorted_dict, file_name_prefix + str(file_suffix))
            file_suffix += 1

        # do n sort file merge
        # get the top X numbers from the final file
        self.sort_merge_files(x_largest_numbers)
