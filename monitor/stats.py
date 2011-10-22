import sys
import math

from kdrvmon.hardware import Hardware, SerialDataFeed, FileDataFeed
from kdrvmon.vario import Vario

def avg(data):
    return sum(data) / len(data)

def rms(data, value):
    return math.sqrt(avg([(x - value)**2 for x in data]))

def main():
    log = sys.argv[1]
    print "Analizing", log
    feed = FileDataFeed(log)
    feed.realtime = False
    feed.autorewind = False
    feed.open()
    hw = Hardware(feed)

    data = []
    while True:
        t, d = hw.read_serial()
        if t == None:
            break
        if t == "pressure":
            data.append(float(d))

    print "Records read: %s" % len(data)


    mean = avg(data)
    print "  Average:", mean, "pa"

    print "  RMS:", rms(data, mean), "pa"

    # convert to altitude
    vario = Vario()
    data = [vario.pressure_to_alt(x) for x in data]

    mean = avg(data)
    print "  Average:", mean, "m"

    print "  RMS:", rms(data, mean), "m"

main()
