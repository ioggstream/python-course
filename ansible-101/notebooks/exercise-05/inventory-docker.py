#!/usr/bin/env python
#
# Exercise: Complete this inventory script.
#
# Note: this only works with docker-compose containers
#       setting the "com.docker.compose.service" label.
#
from __future__ import print_function

import logging

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

#
# Run this script in jupyter and fix one issue at a time.
#
c = Client(base_url="http://172.17.0.1:2375")


def get_inventory_data(container):
    return {
        "container_name": container["Names"][0][1:],
        "ip_address": container["NetworkSettings"]["Networks"]["bridge"]["IPAddress"],
        "group_name": container["Labels"].get("com.docker.compose.service"),
    }


inventory = {}

for container in c.containers():
    # Use str.format to log the container information.
    host = get_inventory_data(container)
    log.debug("Processing entry: {container_name}\t\t{ip_address}".format(**host))
    group_name = host["group_name"]
    ip_address = host["ip_address"]

    if group_name not in inventory:
        inventory[group_name]= {"hosts": []}

    inventory[group_name]["hosts"].append(ip_address)

