"""
    Simple file management with shutil and globbing
     this section includes handling basic unicode issues

    modules: os, sys, shutil, glob
"""
from __future__ import unicode_literals, print_function
basedir = "/tmp/course"


def simple_path_management():
    """S1 Show multiplatform path management

        goal: sys.platform shows the current operating system
        goal: os.path.normpath fixes the "/" orientation

    """
    # .1- The os.path module seems verbose
    #  but it's the *best* way to manage paths. It's:
    #  - safe
    #  - multiplatform
    # .2- Here we check the operating system
    #  and prepend the right path
    import os
    import sys
    hosts, basedir = "etc/hosts", "/"
    if sys.platform.startswith('win'):
        basedir = 'c:/windows/system32/drivers'
    hosts = os.path.join(basedir, hosts)
    hosts = os.path.normpath(hosts)
    print("Normalized path is", hosts)


def create_and_move_tree():
    """S2

        modules: os.path, shutil, errno
        goal: manage directory trees
        goal: manage basic errors

        os.path can be used to test file existence
        while os and shutil supports basic file operations
        like recursive copy and tree creation.

        We can use exception handlers to check
         what happened.
    """
    from os import makedirs
    from os.path import isdir
    from shutil import copytree, rmtree
    makedirs("/tmp/course/foo/bar")
    assert isdir("/tmp/course/foo/bar")

    try:
        # python2 does not allow to ignore
        #  already existing directories
        #  and raises an OSError
        makedirs("/tmp/course/foo/bar")
    except OSError as e:
        # Just use the errno module to
        #  check the error value
        import errno
        assert e.errno == errno.EEXIST

    copytree("/tmp/course/foo", "/tmp/course/foo2")
    assert isdir("/tmp/course/foo2/bar")
    rmtree("/tmp/course/foo")
    assert not isdir("/tmp/course/foo/bar")
