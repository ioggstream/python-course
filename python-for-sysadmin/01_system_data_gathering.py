""" Python for System Administrators

    Gathering System Data with multiplatform
     and platform-dependent tools like command
     line output and files.

"""
#
# Our code is p3-ready
#
from __future__ import print_function


def grep(needle, fpath):
    """A simple grep implementation

       goal: open() is iterable and don't
             needs splitlines()
       goal: comprehension can filter lists
    """
    return [x for x in open(fpath) if needle in x]


def linux_threads(pid):
    """"Glob emulates shell expansion of * and ?

         goal: use globbing and format
         goal: linux proc structure
         goal: startswith accepts tuple arguments
    """
    import glob
    path = "/proc/{}/task/*/status".format(pid)
    t_info = ('Pid', 'Tgid', 'voluntary')  # this is a tuple!
    for t in glob.glob(path):
        t_info = [x for x in open(t) if x.startswith(t_info)]
        print(t_info)


def multiplatform_stats(count):
    """Get data in a multiplatform way

    """
    import psutil
    import time
    cpu_percent, io_stat, io_stat_0 = 0, 0, 0
    print("cpu%", "iops(r+w)")
    for x in range(-count, 1):
        cpu_percent = psutil.cpu_percent()
        read_io, write_io = psutil.disk_io_counters()[:2]
        io_stat = read_io + write_io
        print(cpu_percent, io_stat - io_stat_0)
        io_stat_0 = io_stat
        if x:
            time.sleep(1)


def multiplatform_stats(count):
    """Multiplatform stats with numpy.array"""
    raise NotImplemented


def sh(cmd, shell=False, timeout=0):
    """"Execute a command returning a line-splitted list

       @param cmd - a command string
       @param shell - run command in a shell
       @param timeout - (for python 3.3+) in seconds

       goal: use sys to check python features
       goal: use subprocess.check_output
    """
    from sys import version_info as python_version
    from subprocess import check_output
    if python_version < (3, 3):
        if timeout:
            raise ValueError("Timeout not supported until Python 3.3")
        output = check_output(cmd.split(), shell=shell)
    else:
        output = check_output(cmd.split(), shell=shell, timeout=timeout)
    return output.splitlines()


def system_info_from_command_output():
    """Exercise: write a multiplatform
        pgrep-like function

       Solution is at the EOF
    """
    def pgrep(expr):
        raise NotImplementedError


def zip_iterables():
    """The zip method joins list elements pairwise
        like a zip fastener
    """
    from sys import version_info as python_version
    a_list = [0, 1, 2, 3]
    b_list = ["a", "b", "c", "d"]
    zipper = zip(a_list, b_list)
    if python_version >= (3,):
        zipper = list(zipper)
    assert zipper == [(0, "a"), (1, "b"), (2, "c"), (3, "d")]


def linux_diskstats(disk):
    """Get I/O information from /proc/diskstats

       @param disk def sda
       goal: usage of time.sleep
       goal: usage of zip
       goal: use string concatenation to increase readability
       goal: use *magic with print+sep, splitting and slicing
    """
    from time import sleep
    info = ('reads reads_merged reads_sectors reads_ms'
            ' writes writes_merged writes_sectors writes_ms'
            ' io_in_progress io_ms_weight').split()
    print(*info[:8], sep="\t")
    old = [0] * 11

    while True:
        disk_l = grep(disk, "/proc/diskstats")
        if len(disk_l) > 1:
            raise ValueError("More than one partition matches!")

        info = disk_l[0].split()
        # the first 3 fields are disk informations
        cur = map(int, info[3:])
        delta = [x - y for (x, y) in zip(cur, old)]
        print(*delta[:8], sep="\t")
        old = cur
        sleep(1)

#
# A more complex exercise using a lot of stuff
#


def system_info_from_command_output_solution():
    """Exercise: write a multiplatform
        pgrep-like function
    """
    def pgrep(expr):
        # linux
        return grep(expr, sh("ps -fe"))

    def wpgrep(expr):
        # windows
        return grep(expr, sh("tasklist"))

    # All explorer.exe processes
    print(wpgrep("explorer.exe"))


def linux_diskstats(disk):
    """Get I/O information from /proc/diskstats

       @param disk def sda
       goal: usage of time.sleep
       goal: usage of dict.setdefault
       goal: use string concatenation to increase readability
       goal: use *magic with print+sep, splitting and slicing
    """
    from time import sleep
    info = ('reads reads_merged reads_sectors reads_ms'
            ' writes writes_merged writes_sectors writes_ms'
            ' io_in_progress io_ms_weight').split()
    print(*info, sep=",")
    old, cur = dict(), dict()
    while True:
        disk_l = grep(disk, "/proc/diskstats")
        for x in disk_l:
            info = x.split()
            # the first 3 fields are disk informations
            part = info[2]
            old.setdefault(part, [0] * 11)
            cur[part] = map(int, info[3:])
            delta = [x - y for x, y in zip(cur[part], old[part])]
            print(*delta, sep=",")
            old[part] = cur[part]
        sleep(1)
