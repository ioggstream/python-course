"""
    See how to use encoding
     and read badly encoded files
     from a vfat filesystem
"""

from __future__ import unicode_literals, print_function


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
         Python2 default encoding is ascii.
    """
    from os.path import join as pjoin
    for i in range(3):
        #  Before encoding I can join unicode strings
        #   and os.path.join
        fpath = '.'.join((prefix, str(i), ext))
        fpath = pjoin(dirname, fpath)
        bytepath = fpath.encode(encoding)
        with open(bytepath, 'wb') as fh:
            # in python3 you always convert to bytes
            fh.write(b"My name is: ")
            fh.write(bytepath)
            fh.write(b"\n")


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
            print("file: {!r}".format(utf_path))
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
