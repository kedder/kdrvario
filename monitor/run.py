#!/usr/bin/env python
import sys
from kdrvmon.gui import Gui
from kdrvmon.hardware import SerialDataFeed, FileDataFeed

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_RATE = 57600

def main():
    if len(sys.argv) == 1:
        feed = SerialDataFeed(SERIAL_PORT, SERIAL_RATE)
    else:
        feed = FileDataFeed(sys.argv[1])

    gui = Gui(feed)
    gui.run()

if __name__ == '__main__':
    main()
