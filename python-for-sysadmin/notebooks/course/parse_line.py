__author__ = "rpolli"


def parse_line(line):
    import re

    _, _, hour, host, _, _, dest = line.split()[:7]
    try:
        dest = re.split(r"[<>]", dest)[1]
    except (IndexError, TypeError):
        dest = None
    return (hour, host, dest)
