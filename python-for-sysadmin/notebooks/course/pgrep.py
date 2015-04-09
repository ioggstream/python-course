__author__ = 'rpolli'
from __future__ import absolute_import
from . import grep, sh


def system_info_from_command_output_solution():
    """Exercise: write a multiplatform
        pgrep-like function
    """
    def pgrep(expr):
        # linux or mac
        return grep(expr, sh("ps -fe"))

    def wpgrep(expr):
        # windows
        return grep(expr, sh("tasklist"))

    # All explorer.exe processes
    print(wpgrep("explorer.exe"))
