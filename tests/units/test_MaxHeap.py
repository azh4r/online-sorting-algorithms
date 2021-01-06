from MaxHeap import MaxHeap

class TestMaxHeap:

    def test_initialize_MaxHeap(self):
        maxHeap = MaxHeap([('aaa', 30),('aab', 20),('aac',40),('aba', 50),('abb',90),('abc', 90)],6)
        result = maxHeap.getValues()
        assert result == [(90, 'abc'), (90, 'abb'), (50, 'aba'), (40, 'aac'), (30, 'aaa'), (20, 'aab')]

    def test_add_element_to_full_MaxHeap(self):
        maxHeap = MaxHeap([('aaa', 30),('aab', 20),('aac',40),('aba', 50),('abb',90),('abc', 90)],6)
        maxHeap.add((45,'fef'))
        result = maxHeap.getValues()
        assert result == [(90, 'abc'), (90, 'abb'), (50, 'aba'), (45, 'fef'), (40, 'aac'), (30, 'aaa')]

    def test_add_element_to_not_full_MaxHeap(self):
        maxHeap = MaxHeap([('aaa', 30),('aac',40),('aba', 50),('abb',90),('abc', 90)],6)
        maxHeap.add((20,'pep'))
        result = maxHeap.getValues()
        assert result == [(90, 'abc'), (90, 'abb'), (50, 'aba'), (40, 'aac'), (30, 'aaa'),(20, 'pep')]