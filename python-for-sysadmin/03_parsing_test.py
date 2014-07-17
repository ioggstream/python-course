""" Python for System Administrators

    Roberto Polli <rpolli@babel.it>

    This file shows how to parse a postfix maillog file.
     maillog traces every incoming and outgoing email using
     different line formats.
"""

#
# Before writing the parser we collect the
#  interesting lines to use as a sample
#  For now we're just interested in the following cases
#  1- a mail is sent
#  2- a mail is delivered
test_str_1 = 'May 31 08:30:55 test-fe1 postfix/smtp[16669]: 7CD8E730020: to=<antani2@example.it>, relay=examplemx2.example.it[222.33.44.555]:25, delay=0.8, delays=0.17/0.01/0.43/0.19, dsn=2.0.0, status=sent(250 ok:  Message 2108406157 accepted)'
test_str_2 = 'May 31 08:30:55 test-fe1 postfix/smtp[16669]: 7CD8E730020: removed'


def test_sent():
    hour, host, destination = parse_line(test_str_1)
    assert hour == '08:30:55'
    assert host == 'test-fe1'
    assert destination == 'antani2@example.it'


def test_delivered():
    hour, host, destination = parse_line(test_str_2)
    assert hour == '08:30:55'
    assert host == 'test-fe1'
    assert destination is None


def parse_line(line):
    """ Complete the parse line function.

        Without watching the solution: ICAgIGltcG9ydCByZQogICAgXywgXywgaG91ciwgaG9zdCwgXywgXywgZGVzdCA9IGxpbmUuc3BsaXQoKVs6N10KICAgIHRyeToKICAgICAgICBkZXN0ID0gcmUuc3BsaXQocidbPD5dJywgZGVzdClbMV0KICAgIGV4Y2VwdDoKICAgICAgICBkZXN0ID0gTm9uZQogICAgcmV0dXJuIChob3VyLCBob3N0LCBkZXN0KQoK"""
    raise NotImplementedError("Write me!")
