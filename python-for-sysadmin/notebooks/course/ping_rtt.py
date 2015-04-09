__author__ = 'rpolli'


def ping_rtt():
    """
       goal: slicing data
       goal: using zip to transpose data
    """
    from . import sh
    import sys
    cmd = "ping -c10 www.google.it"
    if 'win' in sys.platform:
        cmd = "ping -n10 www.google.it"

    ping_output = sh(cmd)
    if 'win' in sys.platform:
        ping_output = [ping_output[6::2] for x in ping_output]
    else:
        ping_output = [ping_output[-4:-1:2] for x in ping_output]
    ttl, rtt = zip(*ping_output)
    return map(float, rtt)
