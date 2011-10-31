from collections import deque
from time import time

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


class UnpredictingKalman(Filter):
    def __init__(self, process_var, measure_var):
        super(UnpredictingKalman, self).__init__()

        self.process_var = process_var
        self.measure_var = measure_var

        self.estimate = 0.0
        self.error = 1.0
        self.last_estimate = 0.0
        self.last_error = 0.0
        self.gain = 0.0

    def filter(self, value):
        # time update
        self.last_estimate = self.estimate
        self.last_error = self.error + self.process_var

        # measurement update
        self.gain = self.last_error / (self.last_error + self.measure_var)
        self.estimate = self.last_estimate + self.gain * (value - self.last_estimate)
        self.error = (1 - self.gain) * self.last_error

        #print "\t".join([str(x) for x in [self.last_estimate, self.gain, self.last_error, self.error]])
        return self.last_estimate;


class AlphaBeta(Filter):
    a = 0;
    b = 0;
    lastpos = 0;
    lastvel = 0;

    lastts = 0;

    def __init__(self, a, b):
        super(AlphaBeta, self).__init__()
        self.a = a;
        self.b = b;

    def filter(self, value):
        now = time()
        if not self.lastts:
            self.lastts = now
            self.lastpos = value;
            return self.lastpos;

        dt = now - self.lastts
        self.lastts = now

        alpha = self.a * dt
        beta = self.b * dt**2

        pos = self.lastpos + self.lastvel * dt
        vel = self.lastvel

        r = value - pos

        pos += alpha * r
        vel += beta * r/dt

        self.lastpos = pos
        self.lastvel = vel

        self.emit('velocity', vel)
        return pos



