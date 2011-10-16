import serial
import time

from event import EventSource

class Hardware(EventSource):
    feed = None

    def __init__(self, feed):
        self.init_listeners()
        self.feed = feed

    def open(self):
        self.feed.open()

    def read(self):
        """Read single log value from serial and distribute to listeners"""
        key, value = self.read_serial()
        if key is None:
            return

        self.emit(key, value)

    def read_serial(self):
        line = self.feed.next()
        if ":" not in line:
            return (None, None)
        items = line.strip().split(':')
        if len(items) > 2:
            return (None, None)
        return items

class SerialDataFeed(object):
    serial = None
    device = None
    rate = None

    def __init__(self, device, rate):
        self.device = device
        self.rate = rate

    def open(self):
        self.serial = serial.Serial(self.device, self.rate, timeout=2)

    def next(self):
        return self.serial.readline().strip()

class FileDataFeed(object):
    fname = None
    lastts = 0
    lastout = 0

    def __init__(self, fname):
        self.fname = fname

    def open(self):
        self.f = open(self.fname)
        self.lastts = 0

    def next(self):
        line = self.f.readline().strip()
        if not line:
            print "EOF reached. rewinding."
            self.open()
            return self.next()
        ts, rec = line.split(':', 1)

        ts = float(ts)

        now = time.time()

        if not self.lastts:
            self.lastts = ts
            self.lastout = now

        signaldelay = ts - self.lastts
        processtime = now - self.lastout
        if signaldelay > processtime:
            time.sleep(signaldelay - processtime)

        self.lastts = ts
        self.lastout = time.time()
        return rec
