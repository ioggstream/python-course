"""
    Exercises and function to be used
     in the Python for System Administrator
     course

    This file is just meant to be imported.
     Students are not required to understand its
     content during the course, though they should
     understand all of that at the end!
"""
from __future__ import print_function, unicode_literals, division


#
# For parsing section
#
test_mail_sent = 'May 31 08:30:55 test-fe1 postfix/smtp[16669]: 7CD8E730020: to=<antani2@example.it>, relay=examplemx2.example.it[222.33.44.555]:25, delay=0.8, delays=0.17/0.01/0.43/0.19, dsn=2.0.0, status=sent(250 ok:  Message 2108406157 accepted)'
test_mail_delivered = 'May 31 08:30:55 test-fe1 postfix/smtp[16669]: 7CD8E730020: removed'

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
            fh.write("My name is: ")
            fh.write(bytepath)
            fh.write("\n")
