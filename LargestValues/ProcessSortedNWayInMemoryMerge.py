from six import iteritems
import FileDownloader
import itertools
from DataFile import DataFile
import heapq
from tqdm import tqdm
from DictHelper import dict_lines, sort_dict
import time
from collections import ChainMap
from operator import itemgetter

# Class to sort merge n file chunks in memory in a n-way merge using heapq
# because each file chunk is sorted in memory (using default Timsort) which has worst case Time complexity of O(NlogN)
# N = total number of records in each chunk.    
# and best case of O(n) and worst case space complexity is O(N) and best case O(1)
#
# Then all in-memory sorted segments are merged using a heapq which has Time complexity of O(NLogK) and space complexity of X
# Where N is the total number of records and K is the number of segements/chunks
# 
class SortedNWayMemoryMerge:

    progress_bar = None
    # result_dict = {}
    sorted_dict_chunks_list = []

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

    # This is the callback method which creates all the sorted segemented dicts to be mergesorted in a 
    # seperate method
    def process_chunk(func_object,object,lines, last_chunk, chunk_size):
        object.progress_bar.update(chunk_size)
        dict_chunk = dict_lines(lines)
        sorted_dict_chunk = sort_dict(dict_chunk)
        object.sorted_dict_chunks_list.append(sorted_dict_chunk)
        if last_chunk:
            object.merge_sort_all_dicts(object.sorted_dict_chunks_list) 
            
    
    def merge_sort_all_dicts(self,sorted_dict_chunks_list):
        # merged_map = ChainMap(*sorted_dict_chunks_list)       
        # merged_dict = dict(merged_map)
        # for c in sorted_dict_chunks_list:
        #     c.items()
        # for c in sorted_dict_chunks_list:
        #     print(c)
        # print('\n')
        # return
        # dicts = [c for c in sorted_dict_chunks_list]
        # dicts2 = {}
        # for c in dicts:
        #     for k,v in c.items():
        #         dicts2[k]=v
        #     print('ending i')
        # print('ending c')
        # for i in dicts2:
        #     print(i)
        # print('helloooooooooooooooooo boy')
        # return

        result_generator = heapq.merge(*[x.items() for x in sorted_dict_chunks_list] , key = lambda item: item[1],reverse=True)
        # Saving only the first X items in merge sorted dict
        sliced_generator = itertools.islice(result_generator, self.x_largest_values)
        result_dict = {c[0]:c[1] for c in sliced_generator}
        # for c in sliced_generator:
        #     print(c)
        #time.sleep(1)
        # write the result
        DataFile.write_file(result_dict, "result_final")
        self.progress_bar.close()           
        for k, v in result_dict.items():
            print(k,v)