from heapq import heapify, heappush, heappushpop, nlargest

# Class to keep a heap with a fixed max size using heapq. 
# this is a min heap but since we only ask for nlargest values once at the end this 
# will function as a MaxHeap for our specific usecase. 
# Heapq is not synchrnoized so only thread can update this
class FixedSizeMaxHeap:
    def __init__(self, list, x_size):
        self.heap = [(element[1], element[0]) for element in list]
        self.length = x_size
        heapify( self.heap)
    
    # here tuple should be value, key
    def add(self, element):
        if len(self.heap) < self.length:
            heappush(self.heap, element)
        else:
            heappushpop(self.heap, element)
    
    # 
    def getValues(self):
        return nlargest(self.length, self.heap)
