from collections import deque
from event import EventSource

class Filter(EventSource):
    def __init__(self):
        self.init_listeners()

    def accept(self, value):
        filtered = self.filter(value)
        self.emit('filtered', filtered)

class MovingAverageFilter(Filter):
    def __init__(self, size):
        super(MovingAverageFilter, self).__init__()

        self.size = size
        self.samples = deque()


    def filter(self, value):
        self.samples.append(float(value))
        if len(self.samples) > self.size:
            self.samples.popleft()
        return sum(self.samples) / len(self.samples)
