import os
import sys
import pprint

def test_tox():
    print("Command: ", sys.argv[0])
    for x in 'PYTHONPATH LD_LIBRARY_PATH'.split():
        print(x, os.environ.get(x))


