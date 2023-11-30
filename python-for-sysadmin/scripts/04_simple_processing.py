"""

"""


def sh(cmd):
    """A quick and dirty check_output wrapper.
    Don't use in production as it won't honor
    quoted spaces like "my document.docx"
    """
    from subprocess import check_output

    return check_output(cmd.split()).splitlines()


def ping_rtt():
    """
    goal: slicing data
    goal: using zip to transpose data
    """
    import sys

    from notebooks.course import sh

    cmd = "ping -c10 www.google.it"
    if "win" in sys.platform:
        cmd = "ping -n10 www.google.it"

    ping_output = sh(cmd)
    if "win" in sys.platform:
        ping_output = [ping_output[6::2] for x in ping_output]
    else:
        ping_output = [ping_output[-4:-1:2] for x in ping_output]
    ttl, rtt = zip(*ping_output)
    return map(float, rtt)


def ping_stats():
    """
    goal: remember to convert to numeric / float
    goal: use scipy
    goal: check stdev
    """
    from scipy import mean, std

    rtt = ping_rtt()
    fmt_s = "stdev: {}, mean: {}, min: {}, max: {}"
    rtt_std, rtt_mean = std(rtt), mean(ping_rtt)
    rtt_max, rtt_min = max(rtt), min(ping_rtt)
    print(fmt_s.format(rtt_std, rtt_mean, rtt_max, rtt_min))


def distributions():
    from collections import defaultdict

    """generate data distribution using set or defaultdict
    """
    distro = {x: rtt.count(x) for x in set(rtt)}
    # or
    distro = defaultdict(int)
    for x in rtt:
        distro += 1


def netfishing_correlation():
    from itertools import combinations

    from course import table
    from scipy.stats.stats import pearsonr

    """table = {
        'cpu_percent': [10, 23, 55, ...]
        'iops': [2132, 3212, 3942, ...]
        'netio': [1.32e+9, 1.45e+9, ...]
    }
    """
    for k1, k2 in combinations(table, 2):
        r_coeff, probability = pearsonr(table[k1], table[k2])
        print("linear correlation between {} and {} is {}".format(k1, k2, r_coeff))


def netfishing_correlation_plot():
    from itertools import combinations

    from course import table
    from matplotlib import pyplot as plt
    from scipy.stats.stats import pearsonr

    for (k1, v1), (k2, v2) in combinations(table.items(), 2):
        r_coeff, probability = pearsonr(table[k1], table[k2])
        if r_coeff < 0.6:
            continue
        plt.scatter(v1, v2)
        plt.xlabel(k1)
        plt.ylabel(k2)
        plt.title("r={:0.3f} p={:0.3f}".format(r_coeff, probability))
        plt.savefig("monochromo_{}_{}.png".format(k1, k2))
        plt.close()


def netfishing_correlation_colored_plot():
    from itertools import combinations, cycle

    from course import in_chunks, table
    from matplotlib import pyplot as plt
    from scipy.stats.stats import pearsonr

    max_color, nbins = 1 << 23, 12
    colors = cycle(
        "#" + format(x, "06X") for x in range(0, max_color, max_color / nbins)
    )

    for (k1, v1), (k2, v2) in combinations(table.items(), 2):
        r_coeff, probability = pearsonr(table[k1], table[k2])
        if r_coeff < 0.6:
            continue
        l = len(v1) / nbins
        chunks = zip(in_chunks(v1, l), in_chunks(v2, l))
        [plt.scatter(c1, c2, color=next(colors)) for c1, c2 in chunks]
        plt.xlabel(k1)
        plt.ylabel(k2)
        plt.title("r={:0.3f} p={:0.3f}".format(r_coeff, probability))
        plt.savefig("tmp_{}_{}.png".format(k1, k2))
        plt.close()
