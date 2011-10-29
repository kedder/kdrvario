#!/usr/bin/env python
import sys
import time

from kdrvmon.hardware import SerialDataFeed

first_ts = 0
last_ts = 0
cnt = 0

def log(serial, out):
    global cnt
    global first_ts
    global last_ts

    started = False

    while True:
        rec = serial.next()

        # skip records until hw initialized
        if "Initialization completed." in rec:
            print "Received initialization event. Starting logging."
            started = True
        if not started:
            continue

        now = time.time()

        if not first_ts:
            first_ts = now
        last_ts = now

        out.write("%.5f:%s\n" % (now, rec))
        cnt += 1

        if cnt % 100 == 0:
            print "%s record logged" % cnt

def print_stats():
    totaltime = last_ts - first_ts
    rate = totaltime / cnt
    print "Total samples recorded: %s" % cnt
    print "Total time recorded: %.2f" % totaltime
    print "Data rate: %.2f" % (1/rate)

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
        print_stats()
        print
        print "Exiting."
        out.close()


if __name__ == '__main__':
    main()
