
class PriorityQueue:
    """Array-based priority queue implementation."""
    """ MODIFIED to be heap implementation"""

    def __init__(self):
        """Initially empty priority queue."""
        self.queue = []
        self.size = 0

    def __len__(self):
        # Number of elements in the queue.
        return self.size

    def swap(self, int1, int2):
        temp_val = self.queue[int2]
        self.queue[int2] = self.queue[int1]
        self.queue[int1] = temp_val

    def append(self, key):
        """Inserts an element in the priority queue."""
        if key is None:
            raise ValueError('Cannot insert None in the queue')
        cur_index = self.size;
        self.size += 1
        self.queue.append(key)
        while cur_index != 0 and self.queue[cur_index] < self.queue[(cur_index-1) // 2]:
            self.swap(cur_index, (cur_index - 1) // 2);
            cur_index = (cur_index - 1) // 2

    def min(self):
        """The smallest element in the queue."""
        if self.size == 0:
            return None
        return self.queue[0]

    def pop(self):
        """Removes the minimum element in the queue.

        Returns:
            The value of the removed element.
        """
        if self.size == 0:
            return None
        elif self.size == 1:
            self.size = 0
            return self.queue.pop()
        popped_key = self.queue[0]
        self.queue[0] = self.queue.pop()
        self.size += (-1)
        cur_index = 0
        while 2 * cur_index + 1 < self.size:
            if 2 * cur_index + 2 < self.size:
                if self.queue[cur_index] > min(self.queue[cur_index * 2 + 1], self.queue[cur_index * 2 + 2]):
                    if self.queue[cur_index * 2 + 2] > self.queue[cur_index * 2 + 1]:
                        self.swap(cur_index * 2 + 1, cur_index)
                        cur_index = cur_index * 2 + 1
                    else:
                        self.swap(cur_index * 2 + 2, cur_index)
                        cur_index = cur_index * 2 + 2
                else:
                    break
            else:
                if self.queue[cur_index] > self.queue[cur_index * 2 + 1]:
                    self.swap(cur_index * 2 + 1, cur_index)
                    cur_index = cur_index * 2 + 1
                else:
                    break
        return popped_key

    def print(self):
        print(self.queue)

pq = PriorityQueue()
pq.append(1)
pq.append(2)
pq.append(5)
pq.append(-3)
pq.append(13)
pq.append(103)
pq.append(-23)
pq.append(13)
pq.append(1023)
print(pq.pop())
print(pq.pop())
print(pq.pop())
print(pq.pop())
print(pq.pop())
print(pq.pop())
print(pq.pop())
print(pq.pop())
