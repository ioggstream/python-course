"""Introduction to nosetests - 01

   Run this script with
    #nosetest -v scriptname.py
"""


def setup():
    print("This function is run before the testlist")


def test_one():
    # just name a function like test_* to execute it!
    a = 1
    assert a == 1


def test_two():
    # This test fails and the backtrace is printed
    a = 2
    assert a == 1, "Expecting a == 1. Was %r" % a


def teardown():
    print("after all tests")
