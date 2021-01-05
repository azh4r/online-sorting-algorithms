from ProcessSortedMemoryMerges import SortedMemoryMerge
from unittest import mock


class TestSortedMemoryMerges:
    # Test the process_chunk function which repteadely merges two dicts using a heapq.merge until
    # we have the largest values. This is the core of the logic
    class noprogress_bar:
        def update(size):
            return None
        def close():
            return None

    @mock.patch('ProcessSortedMemoryMerges.SortedMemoryMerge.progress_bar',noprogress_bar)
    def test_SortedMemoryMerges_process_intermediate_chunks(self):
        sortedMemoryMerge = SortedMemoryMerge()
        sortedMemoryMerge.result_dict = {}
        sortedMemoryMerge.x_largest_values = 2
        sortedMemoryMerge.process_chunk(sortedMemoryMerge,['aaa 30','aab 20','aac 40','aba 50','abb 60','abc 90'], False, 8)
        sortedMemoryMerge.process_chunk(sortedMemoryMerge,['aca 80','acb 15','acc 81'], False, 8)
        results = sortedMemoryMerge.result_dict
        assert results == {'abc':90,'acc':81}

    @mock.patch('ProcessSortedMemoryMerges.SortedMemoryMerge.progress_bar',noprogress_bar)
    def test_SortedMemoryMerges_process_last_chunk(requests_mock):
        sortedMemoryMerge = SortedMemoryMerge()
        sortedMemoryMerge.result_dict = {'abc':90,'acc':81}
        sortedMemoryMerge.x_largest_values = 2
        sortedMemoryMerge.process_chunk(sortedMemoryMerge,['aca 80','acb 15','acd 91'], True, 8)
        results = sortedMemoryMerge.result_dict
        assert results == {'acd':91,'abc':90}
