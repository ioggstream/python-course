# Docker connectors


```mermaid
graph LR

subgraph docker[docker fab:fa-docker]
subgraph pad[ ]
c1[container1 fa:fa-cube]
c2[container2 fa:fa-cube]
s1((IP 1 fa:fa-network-wired))
s2((IP 2 fa:fa-network-wired))
end
dockerds((docker\nIP fa:fa-network-wired))
dockerd[[Docker\nserver\n fa:fa-cogs fab:fa-docker]]
end
s1 -.-> c1
s2 -.-> c2

subgraph ansible_connection
ssh-inventory[ssh module fa:fa-lock]
docker-inventory[docker module fab:fa-docker]
end

ssh-inventory -->|ssh| s1 & s2
docker-inventory -->|docker| dockerds
dockerds -->dockerd
c1 & c2 ---|<| dockerd

```

# Ansible architecture

```mermaid
graph

vault[vault fa:fa-lock]
keys[ssh keys fa:fa-key]
subgraph ansible.cfg[ansible.cfg fa:fa-file ]
other
vault_config
auth_config
end

subgraph inventory[inventory fa:fa-file / fa:fa-globe]
s1[prod fa:fa-server]
s2[test fa:fa-server]
s3[other... fa:fa-server]
end

subgraph group_vars[group_vars fa:fa-folder / fa:fa-globe ]
gv1[prod]
gv2[test]
end

ansible.cfg -->|references| inventory
s1 -.- gv1
s2 -.- gv2

vault_config --> vault
auth_config --> keys

ansible.cfg --->|references| modules & roles[roles fa:fa-folder]
```


# IaC

```mermaid
---
title: Infrastructure as Code
---
graph LR

dev(("&nbsp;&nbsp;fa:fa-user fa:fa-laptop&nbsp;&nbsp;\ndev&nbsp;"))
--> |fa:fa-code-pull-request\npull request| repo[(fa:fa-code\nrepository\nscripts\ntemplates\nhosts)]
--> engine

engine --- |>\nOK| infrastructure
dev ---|<\nKO|engine
engine -.-o|get data| ITSM[ITSM fa:fa-server fa:fa-gears]
subgraph engine[IaC Engine fa:fa-gears]
analysis
--- validation{check}
--- deployment
end

subgraph infrastructure[Infrastructure]
direction TB
prod["Production\nfa:fa-server fa:fa-server fa:fa-server
fa:fa-database fa:fa-database fa:fa-database
fa:fa-network-wired fa:fa-network-wired fa:fa-network-wired"]
test["Test\nfa:fa-server fa:fa-server fa:fa-server
fa:fa-database fa:fa-database fa:fa-database
fa:fa-network-wired fa:fa-network-wired fa:fa-network-wired"]
end

linkStyle 3 stroke:red
linkStyle 2 stroke:green
```

# Ansible

- a static or dynamic inventory of all the nodes to manage
- ssh keys to use
- users and secrets to connect to the hosts
- whether to do privilege escalation (eg. sudo, ...) before running tasks
- if nodes should be accessed via a bastion host, docker, ...
