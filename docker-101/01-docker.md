
# Docker 101 - Containerization as an application packaging mechanism

Docker is more than containers:
it is a platform for developers and sysadmins to develop,
ship, and run applications.

---

## Why it was born?

To resolve the needs of mobility workload in cloud systems

- Cargo transport pre-1960
- Solution: Intermodal Shipping Container

[![Cargo ship](https://zegetech.com/assets/images/blog/docker/docker_ship.png)]

---

### Docker is a Container System for Code

Docker leverages LXC (Linux Containers), which encompasses Linux
features like cgroups and namespaces for strong process isolation and
resource control.

They are lightweight and consume less resources than a virtual machine.

---

## Benefits for developers

- portability, build once... run anywhere
- no worries about missing dependencies, packages and other pain
 points during subsequent deployments
- tracking changes
- run each app in its own isolated container, so you can run various
 versions of libraries and other dependencies for each app without
 worrying
- reduce/eliminate concerns about compatibility on different
 platforms, either your own or your customers'.

---

## Benefits for sysadmins

- portability, configure once... run anywhere
- tracking changes
- simple to understand what application do
- simplify to upgrade application processes. Significantly improves
 the speed and reliability of continuous deployment and continuous
 integration systems
- eliminate inconsistencies between different enviroments (develop, testing, production)
- re-use other people images
- do you not need an hypervisor. Because the containers are so
 lightweight, address significant performance, costs, deployment, and
 portability issues normally associated with VMs

---

## Docker Concepts and Interactions

- **Host**, the machine that runs the containers.
- **Image**, a hierarchy of files, with meta-data for running a container.
- **Container**, a contained running process, started from an image.
- **Registry**, a repository of images.
- **Volume**, storage outside the container.
- **Dockerfile**, instruction for creating images.

----

[![](https://mermaid.ink/img/pako:eNptU8lu2zAQ_RWBZ8moZctVdOilKdAeekmBHirmMJLGFhMuAjkM6lr-91JbbCcBD3qjefM4G0-sNg2ygiVJwjUJklhE96Z-RhsJTWihJmG043okHCx0LddcO1-NOHrAg3Bkj-UDKkP4akd7qIo9JM2o9ci1WJec_VBwQBd8g6v2FTo-qM1ci00LtET6ymvyi_UEL7Dg7kit0ZwFVdTNTTrfjSOupwL2QmJ5gfOtM7xN7sVIr9CVv6fvTG2AoAKHgVAbTSA0WleWX1_xVSGPgSRNDTJUMXfkfbGXhIdzlVqSfOkrL2TTR7cigyfqCQ5vHdcpTaTaKCXoA4HBab3uo0vE2-hemdDsPpr78M7tCCzFjkwXWxyNWzWuh8aP1M67NgxVDMVf195fVmOiSfkxbRohi5lCq0A0YTlPXEcRZ9SiQs6KABvcg5fEGdfnQPVdmBV-awQZywqyHmMGnsyvo64Xe-LcCwiboli4ULrwtwP9xxi1kILJihP7y4p1lq-263SzyfI83WTp5zRmR1akd7vVLrvb5Vm-2W6zcM4x-zcqfFplMcMxh5_Toxrf1vk_Byk2hw?type=png)](https://mermaid.live/edit#pako:eNptU8lu2zAQ_RWBZ8moZctVdOilKdAeekmBHirmMJLGFhMuAjkM6lr-91JbbCcBD3qjefM4G0-sNg2ygiVJwjUJklhE96Z-RhsJTWihJmG043okHCx0LddcO1-NOHrAg3Bkj-UDKkP4akd7qIo9JM2o9ci1WJec_VBwQBd8g6v2FTo-qM1ci00LtET6ymvyi_UEL7Dg7kit0ZwFVdTNTTrfjSOupwL2QmJ5gfOtM7xN7sVIr9CVv6fvTG2AoAKHgVAbTSA0WleWX1_xVSGPgSRNDTJUMXfkfbGXhIdzlVqSfOkrL2TTR7cigyfqCQ5vHdcpTaTaKCXoA4HBab3uo0vE2-hemdDsPpr78M7tCCzFjkwXWxyNWzWuh8aP1M67NgxVDMVf195fVmOiSfkxbRohi5lCq0A0YTlPXEcRZ9SiQs6KABvcg5fEGdfnQPVdmBV-awQZywqyHmMGnsyvo64Xe-LcCwiboli4ULrwtwP9xxi1kILJihP7y4p1lq-263SzyfI83WTp5zRmR1akd7vVLrvb5Vm-2W6zcM4x-zcqfFplMcMxh5_Toxrf1vk_Byk2hw)

---

## Separation of concerns

- inside the container:
  - libreries
  - package manager
  - application
  - data
  - code
- outside the container:
  - logging
  - remote access
  - network configuration
  - monitoring

---
