#!/usr/bin/env python
from kdrvmon.gui import Gui
from kdrvmon.hardware import SerialDataFeed, FileDataFeed

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_RATE = 57600

def main():
    feed = SerialDataFeed(SERIAL_PORT, SERIAL_RATE)
    #feed = FileDataFeed('../data/test.out')
    gui = Gui(feed)
    gui.run()

if __name__ == '__main__':
    main()
