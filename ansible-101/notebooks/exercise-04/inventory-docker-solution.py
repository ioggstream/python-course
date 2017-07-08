#!/usr/bin/env python
# List our containers. Note: this only works with docker-compose containers.
from __future__ import print_function
from collections import defaultdict
import json


# 
# Manage different docker libraries
#
try:
    from docker import Client
except ImportError:
    from docker import APIClient as Client

import logging
log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

def print_hosts():
    c=Client(base_url="http://172.17.0.1:2375")
    container_fmt = lambda x: (
        x['Names'][0][1:],
        x['Labels']['com.docker.compose.service'], 
        x['NetworkSettings']['Networks']['bridge']['IPAddress'],
    )
    
    inventory = dict() 
    
    for x in c.containers():
        log.debug("Processing entry %r", '\t\t'.join(container_fmt(x)))
        group_name = x['Labels']['com.docker.compose.service']
        ip_address = x['NetworkSettings']['Networks']['bridge']['IPAddress']
        inventory[group_name] = defaultdict(list)
        inventory[group_name]['hosts'].append(ip_address)
    
    inventory['web']['host_vars'] = {'ansible_ssh_common_args': ' -o StrictHostKeyChecking=no '}
    ret = json.dumps(inventory, indent=True)
    return ret


if __name__ == '__main__':
    print(print_hosts())
