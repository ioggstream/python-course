"""Python for System Administrators

    Exercises
- write the parse_maillog function, bench with %timeit

"""


def test_drive_parsing():

    testline = "May 31 08:30:55 test-fe1 postfix/smtp[16669]: 7CD8E730020: removed"

    def test_one():
        ret = parse_maillog(testline)
        assert ret == ('08:30:55', 'test-fe1', '7CD8E730020'), "Error %r" % ret


def grep(expr, fpath):
    """grep reloaded with regular expressions and path normalization

        GOAL: re.search matches anywhere (eg. '.*XXX.*')
                re.match matches from the beginning of the line.

    """
    import re
    import os
    re_expr = re.compile(expr)
    fpath = os.path.normpath(fpath)
    with open(fpath) as fp:
        return [x for x in fp if re_expr.search(x)]


def splitting_with_re():
    """Splitting with re.split
    """
    import re
    cmd = "ping -c10 -w10 www.google.it"
    # on windows "ping -n10 www.google.it"
    ping_output = sh(cmd)
    ping_output = [re.split("[ =", x) for x in ping_output]


def splitting_with_findall():
    """re.findall for splitting: a shortcut or a misuse?

       goal: improve string readability
    """
    from re import findall  # can be misused too;
    # eg for adding the ":" to a
    mac_address = "00""24""e8""b4""33""20"
    re_s_1 = "[0-9a-fA-F]"
    mac = ':'.join(re.findall(re_s_1, mac))
    print("The mac address is ", mac)


def testing_regexps():
    """time the above exercise replacing re_s_1 with the followings
    """
    test_all_regexps = ("..", "[a-f0-9]{2}")
    for re_s in test_all_regexps:
        %timeit ':'.join(re.findall(re_s, mac))


def fcswitch_configuration_script():
    """Generate a vsan configuration using linux fc_informations"""
    fc_id_path = "/sys/class/fc_host/host*/port_name"
    for x in glob.glob(fc_id_path):
        pwwn = open(x).read()  # 0x500143802427e66c
        pwwn = pwwn[2:]
        pwwn = re.findall(r'..', pwwn)
        print("member pwwn ", ':'.join(pwwn))
