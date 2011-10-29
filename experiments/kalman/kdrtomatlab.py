#!/usr/bin/env python
"""
Convert kdr monitor logs to octave format
"""

import sys

VAR_HEADER = """# name: %s
# type: %s
"""

MATRIX_HEADER = """# rows: %s
# columns: %s
"""
def octave_list(name, data):
    print VAR_HEADER % (name, 'matrix')
    print MATRIX_HEADER % (len(data), 1)
    for v in data:
        print v

def octave_scalar(name, data):
    print VAR_HEADER % (name, 'scalar')
    print data

def main():
    # read data
    data = []
    first_ts = 0;
    last_ts = 0;
    for line in sys.stdin.readlines():
        ts,tp,value = line.split(':')
        if tp != 'pressure':
            continue

        data.append(int(value))
        if first_ts == 0:
            first_ts = float(ts)
        last_ts = float(ts)


    # calculate rate
    rate = (last_ts - first_ts) / len(data)

    # output variables
    octave_list('data', data)
    octave_scalar('dt', rate)

    print "# Total time recorded: %.2f s" % ((last_ts - first_ts))
    print "# Data rate: %.2f Hz" % (1/rate);
    
main()
