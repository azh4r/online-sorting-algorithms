from LargestValues import LargestValues
from unittest import mock


class TestLargestValues:
    # Test the process_chunk function which repteadely merges two dicts using a heapq.merge until
    # we have the largest values. This is the core of the logic
    class noprogress_bar:
        def update(size):
            return None
        def close():
            return None

    @mock.patch('LargestValues.LargestValues.progress_bar',noprogress_bar)
    def test_LargestValues_process_intermediate_chunks(self):
        LargestValues.result_dict = {}
        LargestValues.X_largest_values = 2
        LargestValues.process_chunk(['aaa 30','aab 20','aac 40','aba 50','abb 60','abc 90'], False, 8)
        LargestValues.process_chunk(['aca 80','acb 15','acc 81'], False, 8)
        results = LargestValues.result_dict
        assert results == {'abc':90,'acc':81}

    @mock.patch('LargestValues.LargestValues.progress_bar',noprogress_bar)
    def test_LargestValues_process_last_chunk(requests_mock):
        LargestValues.result_dict = {'abc':90,'acc':81}
        LargestValues.X_largest_values = 2
        LargestValues.process_chunk(['aca 80','acb 15','acd 91'], True, 8)
        results = LargestValues.result_dict
        assert results == {'acd':91,'abc':90}
