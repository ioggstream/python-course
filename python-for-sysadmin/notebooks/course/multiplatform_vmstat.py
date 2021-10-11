def multiplatform_vmstat(count):
    """Get data in a multiplatform way

    """
    import time

    import psutil

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
