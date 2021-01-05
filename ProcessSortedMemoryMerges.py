import FileDownloader
from LargestValues import LargestValues
import itertools
from DataFile import DataFile
import heapq
from tqdm import tqdm
from DictHelper import dict_lines, sort_dict
import time


class SortedMemoryMerge:

    progress_bar = None
    x_largest_value = 0

    #def __init__(self):
        #self.progress_bar = None

    def process(self,remote_file_url, chunk_size, offset_bytes, X_largest_values):
        response_handle = FileDownloader.get_response_handle(remote_file_url, offset_bytes)        
        self.x_largest_value = X_largest_values
        self.get_chunks(self,response_handle, chunk_size, offset_bytes)

    def get_chunks(self,response_handle, chunk_size, offset_bytes):
        file_size = int(response_handle.headers.get('content-length', 0))
        self.progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)
        FileDownloader.get_chunks(response_handle, chunk_size, offset_bytes, self.process_chunk)

    def process_chunk(lines, last_chunk, chunk_size):
        SortedMemoryMerge.progress_bar.update(chunk_size)
        dict_chunk = dict_lines(lines)
        sorted_dict_chunk = sort_dict(dict_chunk)
        result_generator = heapq.merge(sorted_dict_chunk.items(), LargestValues.result_dict.items(),
            key = lambda item:item[1], reverse=True)
        # Saving only the first X items in merge sorted dict
        sliced_generator = itertools.islice(result_generator, SortedMemoryMerge.x_largest_value)
        LargestValues.result_dict = {c[0]:c[1] for c in sliced_generator}
        #time.sleep(1)
        if last_chunk:
            # write the result
            DataFile.write_file(LargestValues.result_dict, "result_final")
            SortedMemoryMerge.progress_bar.close()
            for k, v in LargestValues.result_dict.items():
                print(k)