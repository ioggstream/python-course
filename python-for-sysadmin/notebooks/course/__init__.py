"""
    Exercises, functions and other materials for
     the Python for System Administrator course

    This file is just meant to be imported.
     Students are not required to understand its
     content during the course, though they should
     understand all of that at the end!

Pinging example.microsoft.com [192.168.239.132] with 32 bytes of data:
Reply from 192.168.239.132: bytes=32 time=101ms TTL=124
Reply from 192.168.239.132: bytes=32 time=100ms TTL=124
Reply from 192.168.239.132: bytes=32 time=120ms TTL=124
Reply from 192.168.239.132: bytes=32 time=120ms TTL=124

"""
from __future__ import print_function, unicode_literals, division

#
# For hiding course
#
import base64


def show_solution(bcode):
    s = base64.decodestring(bcode)
    print(s.decode())


#
# For parsing section
#
mail_sent = 'May 31 08:00:00 test-fe1 postfix/smtp[16669]: 7CD8E730020: to=<jon@doe.it>, relay=examplemx2.doe.it[222.33.44.555]:25, delay=0.8, delays=0.17/0.01/0.43/0.19, dsn=2.0.0, status=sent(250 ok:  Message 2108406157 accepted)'
mail_delivered = 'May 31 08:00:00 test-fe1 postfix/smtp[16669]: 7CD8E730020: removed'

#
# For enconding section
#


def create_wuerstelstrasse(dirname="/tmp"):
    """Creates 3 files using cp1252 encoding

       @param dirname - The base directory, default '/tmp'
    """
    from os.path import isdir
    win = 'cp1252'
    prefix = "w\u00fcrstelstra\u00dfe"
    assert isdir(dirname), "Directory not found: %s" % dirname
    touch_encoded_filenames(dirname, prefix, encoding=win)


def create_espana(dirname="/tmp"):
    """Creates 3 files using cp1252 encoding

       @param dirname - The base directory, default '/tmp'
    """
    from os.path import isdir
    win = 'cp1252'
    prefix = "Espa\u00e9a"
    assert isdir(dirname), "Directory not found: %s" % dirname
    touch_encoded_filenames(dirname, prefix, encoding=win)


def touch_encoded_filenames(dirname, prefix, ext='txt', encoding='utf-8'):
    """ Create filenames with a given encoding
         Python2 default encoding is ascii.
    """
    from os.path import join as pjoin
    for i in range(3):
        #  Before encoding I can join unicode strings
        #   and os.path.join
        fpath = '.'.join((prefix, str(i), ext))
        fpath = pjoin(dirname, fpath)
        bytepath = fpath.encode(encoding)
        with open(bytepath, 'wb') as fh:
            fh.write(b"My name is: ")
            fh.write(bytepath)
            fh.write(b"\n")


#
# for data gathering section
#
diskstats_headers = ('major minor device'
                     ' reads reads_merged reads_sectors reads_ms'
                     ' writes writes_merged writes_sectors writes_ms'
                     ' io_in_progress io_ms_spent io_ms_weight').split()


def sh(cmd):
    """A quick and dirty check_output wrapper.
        Use shlex to honor quoted spaces
        like "my document.docx"
    """
    from subprocess import check_output
    from shlex import split
    return check_output(split(cmd)).splitlines()


def grep(expr, fpath):
    """grep reloaded with regular expressions and path normalization

        GOAL: re.search matches anywhere (eg. '.*XXX.*')
                re.match matches from the beginning of the line.

    """
    import re
    import os
    re_expr = re.compile(expr)
    fpath = os.path.normpath(fpath)
    with open(fpath) as fp:
        return [x for x in fp if re_expr.search(x)]


#
# data analysis
#
def in_chunks(dataset, size=10):
    """Split dataset in bins of a given size
       @return a generator
    """
    for i in range(0, len(dataset), size):
        yield dataset[i:i+size]


table = {
    # cpu data
    'cpu_wait': (2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 6, 0, 0, 32, 12, 3, 0, 0, 2, 46, 41, 48, 44, 48, 43, 44, 44, 43, 45, 47, 46, 46, 44, 47, 46, 46, 46, 43, 48, 46, 47, 47, 44, 40, 49, 47, 43, 41, 46, 49, 45, 45, 45, 45, 43, 42, 46, 46, 47, 45),
    'cpu_sys': (6, 2, 2, 1, 3, 2, 2, 1, 1, 2, 1, 1, 2, 2, 3, 1, 2, 3, 5, 1, 2, 2, 6, 2, 1, 1, 3, 3, 5, 4, 2, 1, 4, 3, 2, 3, 2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 3, 1, 2, 2, 2, 3, 5, 1, 2, 2, 4, 2, 2, 3, 4, 1, 2, 2, 3, 3, 2, 2, 3),
    'cpu_usr': (23, 9, 7, 6, 7, 8, 9, 5, 5, 3, 7, 4, 4, 4, 9, 6, 10, 14, 16, 8, 7, 5, 12, 9, 11, 7, 47, 15, 6, 11, 6, 5, 8, 7, 9, 8, 10, 4, 3, 2, 6, 7, 2, 5, 5, 3, 7, 3, 6, 3, 3, 5, 14, 9, 4, 10, 8, 4, 6, 7, 4, 4, 4, 9, 12, 5, 4, 3, 4),
    'cpu_id': (69, 90, 92, 93, 90, 87, 88, 94, 95, 96, 91, 93, 95, 92, 88, 93, 88, 83, 79, 86, 92, 93, 49, 78, 85, 92, 50, 80, 43, 44, 44, 49, 39, 46, 46, 44, 46, 49, 48, 50, 47, 47, 49, 48, 48, 49, 46, 49, 46, 49, 49, 48, 41, 42, 47, 45, 47, 48, 44, 46, 47, 49, 49, 46, 42, 46, 48, 49, 49),
    # I/O
    'byte_in': (348, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2832, 220, 0, 0, 0, 0, 2616, 1456, 1060, 768, 2492, 1504, 464, 512, 656, 584, 436, 748, 568, 456, 1088, 352, 564, 1548, 1764, 612, 680, 648, 928, 1128, 2384, 1712, 1240, 1040, 1104, 964, 716, 1076, 804, 792, 940, 960, 872, 540, 488, 544, 568),
    'byte_out': (383, 0, 0, 0, 0, 72, 0, 0, 0, 0, 0, 56, 0, 116, 16, 0, 52, 0, 0, 120, 0, 0, 0, 0, 79, 0, 0, 300, 180, 0, 120, 4, 360, 0, 0, 0, 0, 104, 0, 0, 0, 0, 48, 4, 0, 0, 8, 0, 60, 0, 0, 144, 0, 46, 29, 0, 0, 0, 192, 0, 0, 292, 0, 96, 0, 0, 0, 0, 0),
    # 'paging'
    'swap_in': (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    'swap_out': (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    # 'memory'
    'cache': (2214824, 2215216, 2215068, 2215076, 2215092, 2215108, 2215108, 2215116, 2214856, 2214860, 2214860, 2214864, 2214868, 2214864, 2215100, 2215132, 2215132, 2214888, 2214888, 2214876, 2214880, 2214880, 2215104, 2215128, 2215332, 2215336, 2215020, 2215012, 2215360, 2215576, 2215372, 2215168, 2215128, 2215156, 2214964, 2214956, 2214940, 2215012, 2214980, 2215076, 2214984, 2215000, 2215004, 2214988, 2214972, 2215056, 2214848, 2215092, 2215076, 2214964, 2214956, 2215032, 2215044, 2215060, 2214976, 2215100, 2215292, 2215268, 2215112, 2215044, 2215084, 2215080, 2214984, 2215272, 2215360, 2215276, 2215288, 2215008, 2215140),
    'buff': (375192, 375192, 375192, 375192, 375192, 375196, 375196, 375196, 375196, 375196, 375196, 375200, 375200, 375204, 375204, 375204, 375204, 375204, 375204, 375208, 375208, 375208, 377976, 378196, 378204, 378204, 378204, 378212, 380836, 382292, 383356, 384124, 386636, 388140, 388604, 389116, 389772, 390360, 390796, 391544, 392112, 392568, 393656, 394012, 394576, 396124, 397888, 398496, 399184, 399832, 400664, 401792, 404176, 405888, 407128, 408168, 409272, 410236, 410956, 412032, 412836, 413628, 414568, 415536, 416408, 416948, 417436, 417980, 418544),
    # 'system'
    'irq': (4, 904, 939, 912, 919, 1072, 1072, 868, 873, 945, 1028, 871, 869, 887, 1002, 923, 1091, 1256, 1253, 1009, 934, 940, 2072, 1138, 1050, 972, 1307, 1088, 2060, 1722, 1482, 1339, 2342, 1506, 1231, 1343, 1357, 1368, 1289, 1467, 1314, 1265, 1456, 1156, 1328, 1527, 1671, 1218, 1446, 1280, 1404, 1588, 2091, 1722, 1577, 1466, 1536, 1371, 1349, 1392, 1432, 1480, 1332, 1520, 1547, 1313, 1317, 1325, 1247),
    'csw': (6, 1651, 1646, 1534, 1647, 1809, 1652, 1361, 1412, 1373, 1419, 1279, 1275, 1453, 1958, 1332, 2610, 3207, 3072, 1764, 1663, 1627, 11546, 2302, 1839, 1486, 1618, 2044, 5631, 4960, 5547, 4245, 7619, 2662, 2870, 3059, 3448, 3241, 3069, 3933, 3270, 2899, 3878, 2603, 2781, 2714, 2569, 2916, 3517, 3014, 3422, 4144, 5855, 5015, 3765, 3627, 4123, 3087, 3466, 2952, 3899, 3878, 2763, 4115, 4178, 3296, 3390, 3423, 3367)
}
