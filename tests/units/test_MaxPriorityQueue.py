from MaxPriorityQueue import MaxPriorityQueue

class TestMaxPriorityQueue:

    def test_add_element_to_MaxPriorityQueue(self):
        maxPriorityQueue = MaxPriorityQueue()
        maxPriorityQueue.push(8,('def','f1'))
        maxPriorityQueue.push(-2,('ksf','f4'))
        maxPriorityQueue.push(23,('dca','f3'))
        maxPriorityQueue.push(1,('abc','f2'))

        assert maxPriorityQueue.pop() == (23, ('dca','f3'))
        assert maxPriorityQueue.pop() == (8, ('def', 'f1'))
        assert maxPriorityQueue.pop() == (1, ('abc', 'f2'))
        assert maxPriorityQueue.pop() == (-2, ('ksf','f4'))