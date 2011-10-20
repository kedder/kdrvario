#!/usr/bin/env python
import sys
from kdrvmon.soundcheck import SoundCheck
from kdrvmon.hardware import SerialDataFeed

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_RATE = 57600

def main():
    feed = SerialDataFeed(SERIAL_PORT, SERIAL_RATE)
    gui = SoundCheck(feed)
    gui.run()

if __name__ == '__main__':
    main()
