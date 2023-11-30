__author__ = "rpolli"
from __future__ import absolute_import

from course import sh


def igrep(expr, iterable):
    return [x for x in iterable if expr in x]


def system_info_from_command_output_solution():
    """Exercise: write a multiplatform
    pgrep-like function
    """

    def pgrep(expr):
        # linux or mac
        return igrep(expr, sh("ps -fe"))

    def wpgrep(expr):
        # windows
        return igrep(expr, sh("tasklist"))

    # All explorer.exe processes
    print(wpgrep("explorer.exe"))
