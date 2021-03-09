from MaxHeap import FixedSizeMaxHeap
import FileDownloader
from tqdm import tqdm


# is the best alogirthm for a very large remote file (N is very large) and a small number of *x-largest 
# values* would be to choose the option.  As we stream the data we keep a Max Heap of x-largest values.  
# We compare the streaming N numbers with the top of the heap and if it is greater we insert it into the 
# fixed size heap in logX time. So time complexity is NlogX. While space is O(X) which is the size of the 
# heap.  
# However when x is very small compared and N (lets say 100 compared to Billion) then after some streaming
#  of remote data (lets say 10,000 values) there will be very few merges in the heap. So NlogX will approch 
# N. 

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
