from heapq import heapify, heappush, heappushpop, nlargest

# Class to convert heapq, which is a min heap into max heap with a fixed max size.
# Heapq is not synchrnoized so only thread can update this
class MaxHeap:
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
            
    def getValues(self):
        return nlargest(self.length, self.heap)
