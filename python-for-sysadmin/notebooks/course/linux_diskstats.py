__author__ = 'rpolli'
from __future__ import print_function
from . import grep


def linux_diskstats(disk):
    """Get I/O information from /proc/diskstats

       @param disk def sda
       goal: usage of time.sleep
       goal: usage of dict.setdefault
       goal: use string concatenation to increase readability
       goal: use *magic with print+sep, splitting and slicing
    """
    from time import sleep
    info = ('reads reads_merged reads_sectors reads_ms'
            ' writes writes_merged writes_sectors writes_ms'
            ' io_in_progress io_ms_weight').split()
    print(*info, sep=",")
    old, cur = dict(), dict()
    while True:
        disk_l = grep(disk, "/proc/diskstats")
        for x in disk_l:
            info = x.split()
            # the first 3 fields are disk informations
            part = info[2]
            old.setdefault(part, [0] * 11)
            cur[part] = map(int, info[3:])
            delta = [x - y for x, y in zip(cur[part], old[part])]
            print(*delta, sep=",")
            old[part] = cur[part]
        sleep(1)
