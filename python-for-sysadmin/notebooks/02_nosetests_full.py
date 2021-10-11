"""An articulated nosetest script using classes

   - setup_class() and setup() increase flexibility
"""

import os


class TestB:
    @classmethod
    def setup_class(self):
        # Run once at startup, eg. create database structure
        print("setup testsuite environment")
        open("/tmp/test2.out", "w").write("0")

    @classmethod
    def teardown_class(self):
        # Run once at teardown, eg. drop database
        print("cleanup testsuite environment")
        os.unlink("/tmp/test2.out")

    def setup(self):
        # Before every test, like populate a table
        print("before_every_test")

    def teardown(self):
        # After every test, eg truncate a table
        print("after_every_test")

    def test_a(self):
        assert os.path.isfile("/tmp/test2.out")

    def test_b(self):
        assert False

    def test_c(self):
        def assert_exists(f):
            # Write assertions inside or outside tests.
            assert os.path.isfile(f)

        for f in ["a.txt", "b.txt", "c.txt"]:
            yield assert_exists, f, "Missing file: %r" % f
