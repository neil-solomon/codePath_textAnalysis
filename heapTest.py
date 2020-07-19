import heapq

minHeap = []
heapq.heappush(minHeap, [5,"five"])
heapq.heappush(minHeap, [1,"one"])
heapq.heappush(minHeap, [2,"two"])
heapq.heappush(minHeap, [4,"four"])
heapq.heappush(minHeap, [1,"oNe"])
heapq.heappush(minHeap, [1,"onE"])
heapq.heappush(minHeap, [-1,"negOne"])

while minHeap:
    print(heapq.heappop(minHeap))
