""" Python for System Administrators
    - session 1
"""


def grep(needle, fpath):
    """A simple grep implementation

       goal: open() is iterable
    """
    return [x for x in open(fpath) if needle in x]


def simple_path_management()
    """Show multiplatform path management

        goal: sys.platform shows the current operating system
        goal: os.path.normpath fixes the "/" orientation
    """
    import sys
    import os
        hosts, basedir = "etc/hosts", "/"
        if 'win' in sys.platform:
            basedir = 'c:/windows/system32/drivers'
        hosts = os.path.join(basedir, hosts)
        hosts = os.path.normpath(hosts)
        print("Normalized path is", hosts)


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


def multiplatform_stats():
    """Get data in a multiplatform way

    """
    import psutil
    import time
    cpu_percent, io_stat, io_stat_0 = 0, 0, 0
    print("cpu%", "iops(r+w)")
    while True:
        cpu_percent = psutil.cpu_percent()
        read_io, write_io = psutil.disk_io_counters()[:2]
        io_stat = read_io + write_io
        print(cpu_percent, io_stat - io_stat_0)
        io_stat_0 = io_stat
        time.sleep(1)


def linux_diskstats(disk):
    """Get I/O information from /proc/diskstats

       @param disk def sda
       goal: usage of time.sleep
       goal: use string concatenation to increase readability
       goal: use *magic with print+sep, splitting and slicing
    """
    from time import sleep
    info = ('reads reads_merged reads_sectors reads_ms'
            ' writes writes_merged writes_sectors writes_ms'
            ' io_in_progress io_ms_weight').split()
    print(*info, sep=",")
    old = dict()
    while True:
        disk_l = grep(disk, open("/proc/diskstats"))
        for x in disk_l:
            info = x.split()
            # the first 3 fields are disk informations
            old.setdefault(part, [0] * 11)
            part = info[2]
            info[part] = map(int, info[3:])
            delta = [x - y for x, y in zip(info[part], old[part])]
            print(*delta, sep=",")
            old[part] = info[part]
        sleep(1)


def sh(cmd, timeout=0, shell=False):
    """"Running commands"""
    from subprocess import check_output
    output = check_output(cmd.split(), timeout=timeout, shell=shell)
    return output.splitlines()


def pgrep(expr):
    return grep(expr, sh("ps -fe"))


def wpgrep(expr):
    return grep(expr, sh("tasklist"))

print(wpgrep("explorer.exe"))
