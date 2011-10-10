import serial
class Stream(object):
    serial = None

    def __init__(self, device, rate):
        self.serial = serial.Serial(device, rate)


    def read(self):
        line = self.serial.readline()
        if ":" not in line:
            return (None, None)
        return line.strip().split(':')
