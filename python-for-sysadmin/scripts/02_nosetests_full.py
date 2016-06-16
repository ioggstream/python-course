"""An articulated nosetest script using classes

   - setup_class() and setup() increase flexibility
"""

import os
import errno

# Import assert_* tools
from nose.tools import *

class TestB(object):

    @classmethod
    def setup_class(self):
        # Run once at startup, eg. create database structure
        print("\nsetup testsuite environment")
        open("/tmp/test2.out", "w").write("0")

    @classmethod
    def teardown_class(self):
        # Run once at teardown, eg. drop database
        print("\ncleanup testsuite environment")
        os.unlink("/tmp/test2.out")

    def setup(self):
        # Before every test, like populate a table
        print("\nbefore_every_test")

    def teardown(self):
        # After every test, eg truncate a table
        print("\nafter_every_test")

    def test_a(self):
        assert os.path.isfile("/tmp/test2.out")

    def test_b(self):
        assert False

    #
    # Bonus examples:
    #
    #   - testing exceptions
    #   - parametrized tests 
    #
    @raises(IOError)
    def test_except(self):
        assert open('/tmp/MISSING')

    def test_except_complex(self):
        with assert_raises(IOError) as ex:
            fh = open('/tmp/MISSING')
        # Verify exception *and* errno!
        assert_equals(ex.exception.errno, errno.ENOENT)

    def test_parametrized(self):
        # Runs 3 tests using the nosetest generator syntax.
        for i in range(3):
            # You have to yield a method to make it work into 
            #  a class
            yield self.harn_greater, i, 0 

    def harn_greater(self, a, b):
        assert_greater(a, b)

