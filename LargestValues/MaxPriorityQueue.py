from queue import PriorityQueue

# by default python PriorityQueue is a Min PriorityQueue, this will reverse the priority to 
# make it into a max priority queue
class MaxPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.reverse = -1 

    def push(self, priority, data):
        PriorityQueue.put(self,(self.reverse*priority, data))

    def pop(self, *args, **kwargs):
        priority, data = PriorityQueue.get(self, *args, **kwargs)
        return self.reverse * priority, data


