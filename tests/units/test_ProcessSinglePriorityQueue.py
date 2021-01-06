from MaxHeap import MaxHeap
from DataFile import DataFile
from ProcessSinglePriorityQueue import SinglePriorityQueueMerges
from unittest import mock


class TestSinglePriorityQueueMerges:
    # Test the process_chunk function which repteadely merges two dicts using a heapq.merge until
    # we have the largest values. This is the core of the logic
    class noprogress_bar:
        def update(size):
            return None
        def close():
            return None

    # class nodatafile:
    #     def write_file(sorted_dict, file_name):
    #         return None

    @mock.patch('ProcessSinglePriorityQueue.SinglePriorityQueueMerges.progress_bar',noprogress_bar)
    def test_SinglePriorityQueueMerges_process_single_maxheap(self):
        singlePriorityQueueMerge = SinglePriorityQueueMerges()
        singlePriorityQueueMerge.max_heap = MaxHeap([],2)
        singlePriorityQueueMerge.x_largest_values = 2
        singlePriorityQueueMerge.process_single_maxheap(singlePriorityQueueMerge,['aaa 30','aab 20','aac 40','aba 50','abb 60','abc 90'], False, 8)
        singlePriorityQueueMerge.process_single_maxheap(singlePriorityQueueMerge,['aca 80','acb 15','acc 81'], False, 8)
        results = singlePriorityQueueMerge.max_heap.getValues()
        assert results == [(90, 'abc'),(81, 'acc')]

    @mock.patch('ProcessSinglePriorityQueue.SinglePriorityQueueMerges.progress_bar',noprogress_bar)
    def test_SortedMemoryMerges_process_last_chunk(self):
        singlePriorityQueueMerge = SinglePriorityQueueMerges()
        singlePriorityQueueMerge.max_heap = MaxHeap([('abc',90),('acc',81)],2)
        singlePriorityQueueMerge.x_largest_values = 2
        singlePriorityQueueMerge.process_single_maxheap(singlePriorityQueueMerge,['aca 80','acb 15','acd 91'], True, 8)
        results = singlePriorityQueueMerge.max_heap.getValues()
        assert results == [(91,'acd'),(90,'abc')]
