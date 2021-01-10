from MaxHeap import FixedSizeMaxHeap
import FileDownloader
from tqdm import tqdm


# This is the best algorithm for getting the x-largest from an extremely large unsorted file. 
# with a small k (x_largest_values) 
# Best algo for k << N 
# Time Complexity N(logk) and will tend to N if k is very small.
# Space Complexity logk 
class SinglePriorityQueueMerges:

    progress_bar = None

    def process(self,remote_file_url, chunk_size, offset_bytes, x_largest_values):
        self.max_heap = FixedSizeMaxHeap([],x_largest_values)
        response_handle = FileDownloader.get_response_handle(remote_file_url, offset_bytes)
        file_size = int(response_handle.headers.get('content-length', 0))
        self.progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)
        FileDownloader.get_chunks(self,response_handle, chunk_size, offset_bytes, self.process_single_maxheap)

    # Callback function
    def process_single_maxheap(object_function,object,lines, last_chunk, chunk_size):
        object.progress_bar.update(chunk_size)
        for line in lines:
            key, value = line.split()
            object.max_heap.add((int(value),key))
        if last_chunk:
            object.progress_bar.close()
            # write the result
            elements = object.max_heap.getValues()
            for elem in elements:
                print(elem[1])
