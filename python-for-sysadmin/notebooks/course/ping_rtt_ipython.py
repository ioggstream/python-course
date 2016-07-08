# If you had issue in solving the exercise,
# use ipython to get the data with
def ping_rtt():
    # Adapt this for windows: ping parameters and taken fields
    ret = !ping -c10 8.8.8.8
    rtt = ret.grep("time=").fields(-2)
    rtt = [float(x[5:]) for x in rtt]
    return rtt

