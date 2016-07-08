__author__ = 'rpolli'


def ping_rtt():
    """
       goal: slicing data
       goal: using zip to transpose data
    """
    from course import sh
    import sys
    cmd = "ping -c10 www.google.it"
    if 'win' in sys.platform:
        cmd = "ping -n10 www.google.it"

    ping_output = sh(cmd)
    filter_lines = (x.split() for x in ping_output if 'time' in x)
    if 'win' in sys.platform:
        ping_output = [x[6::2] for x in filter_lines]
    else:
        ping_output = [x[-4:-1:2] for x in filter_lines]
    ttl, rtt = zip(*ping_output)
    return [float(x.split("=")[1]) for x in rtt]

