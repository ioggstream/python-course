#!/usr/bin/env python
# List our containers. Note: this only works with docker-compose containers.
from __future__ import print_function

import json
from collections import defaultdict

#
# Support different docker libraries.
#
try:
    from docker import Client
except ImportError:
    from docker import APIClient as Client

import logging

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


def get_inventory_data(container):
    return {
        "container_name": container["Names"][0][1:],
        "ip_address": container["NetworkSettings"]["Networks"]["bridge"]["IPAddress"],
        "group_name": container["Labels"].get("com.docker.compose.service"),
    }


def create_inventory():
    #
    # Create a Docker client connecting to the docker daemon port.
    #
    c = Client(base_url="http://172.17.0.1:2375")
    inventory = {}

    for container in c.containers():
        # Use str.format to log the container information.
        host = get_inventory_data(container)
        log.debug("Processing entry: {container_name}\t\t{ip_address}".format(**host))

        # Skip parsing errors, and log a warning.
        try:
            group_name = host["group_name"]
            ip_address = host["ip_address"]
            if group_name not in inventory:
                inventory[group_name] = defaultdict(list)
            inventory[group_name]["hosts"].append(ip_address)
        except KeyError:
            log.warning("Host not run via docker-compose: skipping")

    #
    # Replace host variables for the "web" group.
    #
    inventory["web"]["vars"] = {
        "ansible_ssh_common_args": " -o StrictHostKeyChecking=no "
    }
    ret = json.dumps(inventory, indent=True)
    return ret


#
# Execute the script.
#
if __name__ == "__main__":
    inventory_text = create_inventory()
    print(inventory_text)
