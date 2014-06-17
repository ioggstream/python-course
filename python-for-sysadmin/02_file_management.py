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


def encoding_basic():
    """S3
        When the child was a child, 
        strings were a list of bytes.
        In 21th century, that's False (and python2 was mainly
        developed in 20th century;).
        
        bytes is a list of bytes
        A string is a couple: (bytes, encoding).
        
        An encoding is a one-to-one map between a byte-sequence
         and a typographical character.
    """

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

