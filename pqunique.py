import queue
from heapq import heappush, heappop


class UniquePriorityQueue(queue.Queue):
    def __init__(self, *args, key=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key

    def _init(self, maxsize):
        self.keys = set()
        self.queue = []

    def put(self, item, block=True, timeout=None):
        '''Put an item into the queue if it's not already there.

        Returns `True` if the item was not already in the queue, `False`
        otherwise.
        '''

        # TODO: any better way to do this other than copying the whole source?

        with self.not_full:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() >= self.maxsize:
                        raise Full
                elif timeout is None:
                    while self._qsize() >= self.maxsize:
                        self.not_full.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    endtime = time() + timeout
                    while self._qsize() >= self.maxsize:
                        remaining = endtime - time()
                        if remaining <= 0.0:
                            raise Full
                        self.not_full.wait(remaining)
            result = self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
        return result

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        k = self._getkey(item)
        if k not in self.keys:
            self.keys.add(k)
            heappush(self.queue, item)
            return True
        else:
            return False

    def _get(self):
        item = heappop(self.queue)
        k = self._getkey(item)
        self.keys.remove(k)
        return item

    def _getkey(self, item):
        if self.key is not None:
            return self.key(item)
        else:
            return item

if __name__ == '__main__':
    q = queue.PriorityQueue()
    q.put((2, (1, 1)))
    q.put((1, (2, 1)))
    print(q.qsize())
    print(q.get())
    print(q.get())

    q = UniquePriorityQueue(key=lambda v: v[1][1])
    q.put((2, (1, 1)))
    q.put((1, (2, 1)))
    print(q.qsize())
    print(q.get())
