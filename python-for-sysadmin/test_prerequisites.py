"""Test Python for System Administrator Prerequisites

   usage: nosetests -v test_prerequisites.py

   expected output:

test_prerequisites.test_imports('nose',) ... ok
test_prerequisites.test_imports('psutil',) ... ok
test_prerequisites.test_imports('scipy',) ... ok
test_prerequisites.test_imports('matplotlib',) ... ok
test_prerequisites.test_imports('numpy',) ... ok

----------------------------------------------------------------------
Ran 5 tests in 1.634s

OK

"""
import importlib


def harn_import(l):
    importlib.import_module(l)


def test_imports():
    required = "nose psutil scipy matplotlib numpy".split()
    for m in required:
        yield harn_import, m
