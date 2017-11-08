#!/usr/bin/env python
# List our containers. Note: this only works with docker-compose containers.
from __future__ import print_function
from collections import defaultdict
import json
import docker
import logging
log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)



c = Client(base_url="http://172.17.0.1:2375")


container_fmt = lambda x: (
    x['Names'][0][1:],
    x['Labels']['com.docker.compose.service'], 
    x['NetworkSettings']['Networks']['bridge']['IPAddress'],
)

inventory = defaultdict(list)

for x in c.containers():
    log.debug("Processing entry %r", '\t\t'.join(container_fmt(x)))
    group_name = x['Labels']['com.docker.compose.service']
    ip_address = x['NetworkSettings']['Networks']['bridge']['IPAddress']
    inventory[group_name].append(ip_address)

