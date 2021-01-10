import FileDownloader
from LargestValues import LargestValues
import itertools
from DataFile import DataFile
import heapq
from tqdm import tqdm
from DictHelper import dict_lines, sort_dict
import time

# This uses an iterative 2-way merge.  And we use the resultant x-largest numbers as the dict to repeatedly merge 
# the incoming segments with using a heap. So we will still be comaring a total of N records with a heap of k size
# so time complexity of O(Nlog(k)) and space requirments of O(chunk-size)
class SortedMemoryMerge:

    progress_bar = None
    # result_dict = {}

    def __init__(self):
        # not needed
        self.x_largest_values = 0
        self.result_dict = {}

    def process(self,remote_file_url, chunk_size, offset_bytes, X_largest_values):
        response_handle = FileDownloader.get_response_handle(remote_file_url, offset_bytes)        
        self.x_largest_values = X_largest_values
        self.get_chunks(response_handle, chunk_size, offset_bytes)

    def get_chunks(self,response_handle, chunk_size, offset_bytes):
        file_size = int(response_handle.headers.get('content-length', 0))
        self.progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)
        FileDownloader.get_chunks(self,response_handle, chunk_size, offset_bytes, self.process_chunk)

    # Callback method which merges one chunk at a time as it is returned from the FileDownloader.
    # This should be more memory/space efficient than a n-chunks in-memory merge. Space/Storage complexity : O(chunk-size)
    # But time-comlexity O(Nlogk) will be higher than a n-chunk in-memory merge but it depends on size of x-largest result (k).  If k is small 
    # this maybe faster
    def process_chunk(func_object,object,lines, last_chunk, chunk_size):
        object.progress_bar.update(chunk_size)
        dict_chunk = dict_lines(lines)
        sorted_dict_chunk = sort_dict(dict_chunk)
        # for c in sorted_dict_chunk:
        #         print(c)
        # return

        result_generator = heapq.merge(sorted_dict_chunk.items(), object.result_dict.items(),
            key = lambda item:item[1], reverse=True)
        # Saving only the first X items in merge sorted dict
        sliced_generator = itertools.islice(result_generator, object.x_largest_values)
        # for c in sliced_generator:
        #     print (c)
        object.result_dict = {c[0]:c[1] for c in sliced_generator}

        #time.sleep(1)
        if last_chunk:
            # write the result
            #DataFile.write_file(object.result_dict, "result_final")
            object.progress_bar.close()
            for k, v in object.result_dict.items():
                print(k, v)