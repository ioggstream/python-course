#!/usr/bin/env python
#
# Exercise: Complete this inventory script.
#
# Note: this only works with docker-compose containers
#       setting the "com.docker.compose.service" label.
#
from __future__ import print_function

import logging
from collections import defaultdict

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


c = Client(base_url="http://172.17.0.1:2375")


def get_inventory_data(container):
    return {
        "container_name": container["Names"][0][1:],
        "ip_address": container["NetworkSettings"]["Networks"]["bridge"]["IPAddress"],
        "group_name": container["Labels"].get("com.docker.compose.service"),
    }


inventory = defaultdict(list)

for container in c.containers():
    # Use str.format to log the container information.
    host = get_inventory_data(container)
    log.debug("Processing entry: {container_name}\t\t{ip_address}".format(**host))
    group_name = host["group_name"]
    ip_address = host["ip_address"]
    inventory[group_name].append(ip_address)
