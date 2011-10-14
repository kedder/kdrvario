from collections import deque
from time import time

from event import EventSource

VARIO_LAG = 15  # samples
STD_PRESSURE = 101325.0 # Pa

class Vario(EventSource):
    pressure = 0
    altitude = 0
    vario = 0

    history = None

    def __init__(self):
        self.init_listeners()
        self.history = deque()

    def on_pressure(self, key, pressure):
        self.pressure = pressure
        self.altitude = self.pressure_to_alt(pressure)

        now = time()
        self.history.append((now, self.altitude))
        if len(self.history) > VARIO_LAG:
            lastts, lastalt = self.history.popleft()
            self.calculate_vario(lastts, lastalt, now, self.altitude)

    def pressure_to_alt(self, pressure):
        return 44330 * (1 - (pressure/STD_PRESSURE) ** (1/5.255))

    def calculate_vario(self, lastts, lastalt, now, altitude):
        timedelta = now - lastts
        altdelta = altitude - lastalt
        self.vario = altdelta / timedelta
        self.emit("vario", self.vario)
