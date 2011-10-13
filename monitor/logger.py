#!/usr/bin/env python
import sys
import time

from kdrvmon.hardware import SerialDataFeed


def log(serial, out):
    cnt = 0
    while True:
        rec = serial.next()
        now = time.time()
        out.write("%.5f:%s\n" % (now, rec))
        cnt += 1

        if cnt % 100 == 0:
            print "%s record logged" % cnt

def main():
    if len(sys.argv) != 2:
        print "Error! Provide file name to log to."
        return

    fname = sys.argv[1]

    print "KDRVario logger"
    print

    out = file(fname, "w")
    print "Logging serial output to %s" % fname

    serial = SerialDataFeed('/dev/ttyACM0', 57600);
    serial.open()
    print "Serial port opened."


    try:
        log(serial, out)
    except KeyboardInterrupt:
        print
        print "Exiting."
        out.close()


if __name__ == '__main__':
    main()
