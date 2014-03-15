"""
    Simple file management with shutil and globbing
     this section includes handling basic unicode issues
"""
from __future__ import unicode_literals, print_function
basedir = "/tmp/course"


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


def touch_encoded_filenames(dirname, prefix, ext='txt', encoding='utf-8'):
    """ Create filenames with a given encoding
    """
    from os.path import join as pjoin
    for i in range(3):
        #  Before encoding I can join unicode strings
        #   and os.path.join
        fpath = '.'.join((prefix, str(i), ext))
        fpath = pjoin(dirname, fpath)
        bytepath = fpath.encode(encoding)
        open(bytepath, 'w').close()


def windows_filenames():
    """ As filenames are actually binary data
         we should be careful when our scripts read
         eg from a vfat filesystem.

        In this example we're creating 3 windows-encoded
         filenames like wuerstelstrasse.X.txt

        os.path functions fail mangling them as encoded strings
         so we ask it to mangle as bytes.
         moreover we use "{!r}".format to avoid further encoding
         issues in the printing part
    """
    from os.path import join as pjoin
    from os import listdir as ls
    win = 'cp1252'
    prefix = "w\u00fcrstelstra\u00dfe"
    touch_encoded_filenames("/tmp/course", prefix, encoding=win)

    for f in ls(basedir):
        try:
            utf_path = pjoin(basedir, f)
            print("file: {!r}".format(utf_path))
        except UnicodeDecodeError as e:
            print("Error decoding {!r}".format(f))

    bytebasedir = bytes(basedir)
    for b in ls(bytebasedir):
        try:
            byte_path = pjoin(bytebasedir, b)
            print("bytefile: {!r}".format(byte_path))
        except UnicodeDecodeError as e:
            print("Error decoding {!r}".format(b))


def windows_filenames_short():
    """ As filenames are actually binary data
         we should be careful when our scripts read
         eg from a vfat filesystem.

        In this example we're creating 3 windows-encoded
         filenames like wuerstelstrasse.X.txt

        os.path.* and glob.*  fail mangling them as encoded strings
         so we ask it to mangle as bytes.
         moreover we use "{!r}".format to avoid further encoding
         issues in the printing part
    """
    from glob import glob
    from os.path import join as pjoin
    win = 'cp1252'
    prefix = "w\u00fcrstelstra\u00dfe"

    touch_encoded_filenames("/tmp/course", prefix, encoding=win)

    # glob fails while mangling those filenames
    #  as encoded strings
    try:
        files = glob("/tmp/course/*.txt")
    except UnicodeDecodeError as e:
        print("Error decoding files in {!r}".format("/tmp/course"))

    # while everything works fine mangling them as
    #  mere byte-sequences
    for f in glob(b"/tmp/course/*.txt"):
        try:
            print("file: {!r}".format(f))
        except UnicodeDecodeError as e:
            print("Error decoding {!r}".format(f))

