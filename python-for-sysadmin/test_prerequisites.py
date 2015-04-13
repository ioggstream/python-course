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


def harn_import(l, p=None):
    importlib.import_module(l, package=None)


def test_imports():
    required = "nose psutil scipy matplotlib numpy IPython shlex".split()
    for m in required:
        yield harn_import, m


def test_further():
    required = [
        '__future__:print_function  unicode_literals division',
        'collections:defaultdict',
        'glob:glob',
        'itertools:combinations',
        'os:listdir  makedirs',
        'os.path:expanduser isdir join',
        're:findall match',
        'scipy:std  mean',
        'scipy.stats.stats:pearsonr',
        'shutil:copytree  rmtree',
        'subprocess:check_output',
        'sys:version_info',
        'telnetlib:Telnet',
        'matplotlib:pyplot mlab',
        'time:sleep']
    for m in required:
        m, ps = m.split(":", 1)
        for p in ps.split():
            yield harn_import, m, p
