import serial
class Hardware(object):
    serial = None
    listneres = None

    def __init__(self):
        self.listeners = {}

    def open(self, device, rate):
        self.serial = serial.Serial(device, rate)

    def read(self):
        """Read single log value from serial and distribute to listeners"""
        key, value = self._read_serial()
        if key is None:
            return
        if key not in self.listeners:
            return

        for listener in self.listeners[key]:
            listener(key, value)

    def listen(self, key, listener):
        if key not in self.listeners:
            self.listeners[key] = []
        self.listeners[key].append(listener)

    def _read_serial(self):
        line = self.serial.readline()
        if ":" not in line:
            return (None, None)
        return line.strip().split(':')
