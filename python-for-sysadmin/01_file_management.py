"""
    Simple file management with shutil and globbing
     this section includes handling basic unicode issues
"""


def create_and_move_tree():
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
