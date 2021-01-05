from MaxHeap import MaxHeap
import FileDownloader
from tqdm import tqdm


class SinglePriorityQueueMerges:

    progress_bar = None

    def process_maxheap(self,remote_file_url, chunk_size, offset_bytes, x_largest_values):
        self.max_heap = MaxHeap([],x_largest_values)
        response_handle = FileDownloader.get_response_handle(remote_file_url, offset_bytes)
        file_size = int(response_handle.headers.get('content-length', 0))
        self.progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)
        FileDownloader.get_chunks(response_handle, chunk_size, offset_bytes, SinglePriorityQueueMerges.process_single_maxheap)

    # Callback function
    def process_single_maxheap(lines, last_chunk, chunk_size):
        SinglePriorityQueueMerges.progress_bar.update(chunk_size)
        for line in lines:
            key, value = line.split()
            SinglePriorityQueueMerges.max_heap.add((int(value),key))
        if last_chunk:
            SinglePriorityQueueMerges.progress_bar.close()
            # write the result
            elements = SinglePriorityQueueMerges.max_heap.getLargest()
            for elem in elements:
                print(elem[1],' ', elem[0])
