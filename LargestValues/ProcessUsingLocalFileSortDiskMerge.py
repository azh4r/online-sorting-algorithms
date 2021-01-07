from io import TextIOWrapper
from MaxPriorityQueue import MaxPriorityQueue
from DataFile import DataFile
import os, glob, shutil
import DictHelper
import tempfile
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

class LocalFileSortDiskMerge:
    
    def sort_merge_files_from_disk(self, x_largest_numbers):
        # scan all the already sorted out_*.txt files
        #   read the file_name and the first key / first number in the file into the dict. 
        #   Using MaxPriorityQueue now.. which is based on a heap
        #
        #   1.take the max value from the MPQ and put the 'key,value' tuple in a result list
        #       if file has no more lines then close the file handle
        #          if file has more lines then get the next line (key value pair) and push it onto the MPQ.
        #  
        #   Now repeat from 1, until we have the number of max values we want or the MPQ is empty 
        #   result_dict will now have the key,value tuples in order of values.

        result_dict = {}
        number_of_files = len(glob.glob("outfile_*.txt"))
        MaxPQ = MaxPriorityQueue()
        # tempFile = tempfile.NamedTemporaryFile(dir=self.cwd+ '/temp', delete=False)
                                                           
        for file in glob.glob("outfile_*.txt"):
            fp = open(file, 'r')
            key, value = fp.readline().split()
            MaxPQ.push(int(value),[file,key])

        file_dict = {}
        while not MaxPQ.empty() and len(result_dict) < x_largest_numbers:
            value, data = MaxPQ.pop()
            result_dict[data[1]] = int(value)
            filename = data[0]
            if filename not in file_dict:
                file_dict[filename] = open(filename, 'r')
            line = file_dict[filename].readline().strip()
            if not line == '':
                key,value = line.split()
                MaxPQ.push(int(value),[filename,key])
            else:
                file_dict[filename].close()

        for k in file_dict.keys():
            if not file_dict[k].closed:
                file_dict[k].close()
            
        result_file = "result_final_2"
        for k,v in result_dict.items():
            print(k)
            
        DataFile.write_file(result_dict, result_file)

    # read the input file and create local segmented files
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
        self.sort_merge_files_from_disk(x_largest_numbers)