## Inspect the Docker host

At first, we will inspect this machine: the operating system, the IP address and the rest.

```bash
# Distro
cat /etc/issue
```

```bash
# Linux version
uname -a
```

```bash
# IP address
ip -4 -o address show eth0
```

---

## Docker installation

Check that the docker tools are installed on your test environment.

```bash
# Docker CLI version.
docker --version
```

```bash
# Docker server version
dockerd --version
```

---

## Running a container

Docker comes with a catalog of possible operating systems and applications named [Docker Registry](https://hub.docker.com).
You can deploy your custom registry too.

Let's pull (download) and run an image

[![](https://mermaid.ink/img/pako:eNptU8tu2zAQ_BWCQG6SUT_kODr00hRoD70kQA8Vc6DEtcVaXArkMq1r5d9LPRzbScADZ7XD0exyeeSVVcBznqapQNLUQM7ubbUHxzQSOFmRtugFDoSdk20tUKAP5YDZA-y0J3coHsBYgteYbWWZb2WqBq0ngXpeCP7dyB34mOtTVSjBi15t4jpQtaTTyVAGpHCKfstnecLtgWqLgkdVQHVl55v1JHAsYKsbKM5w-usEr8092yYY8MXPcZ-oSpIspYdIqCyS1AjOF8WXV3xRyFMkNbaSTaxi6sj7Ys-G-3VhLU0_d2XQjerYtUifYR3J3dvEpaWRVFljNH0g0CddwI6dT7w93Rkbm92xqQ_v0p6ko8STbRMHQ3CtJrBv_EBtg6_jpeq--Mvau_NojLSm-Zg2XqHAmxvWk5hExaL9uLOBPYuN1rh_pENs3DK5ZVHT7iGP05OMMP2jFdV5xhNuwBmpVRzwo0DGBKcaDAieR6hgK0NDggt8idTQxvuGr0qTdTwnFyDhMpB9PGB1ikfOvZZx2gyPphsfv7YSf1lrTqQY8vzI__J8nm1mq_liucw2m8UyW9wuEn7g-eJuPVtnd-tNtlmuVllcLwn_Nyh8mmUJh8HDj_FhDu_z5T_yHk5s?type=png)](https://mermaid.live/edit#pako:eNptU8tu2zAQ_BWCQG6SUT_kODr00hRoD70kQA8Vc6DEtcVaXArkMq1r5d9LPRzbScADZ7XD0exyeeSVVcBznqapQNLUQM7ubbUHxzQSOFmRtugFDoSdk20tUKAP5YDZA-y0J3coHsBYgteYbWWZb2WqBq0ngXpeCP7dyB34mOtTVSjBi15t4jpQtaTTyVAGpHCKfstnecLtgWqLgkdVQHVl55v1JHAsYKsbKM5w-usEr8092yYY8MXPcZ-oSpIspYdIqCyS1AjOF8WXV3xRyFMkNbaSTaxi6sj7Ys-G-3VhLU0_d2XQjerYtUifYR3J3dvEpaWRVFljNH0g0CddwI6dT7w93Rkbm92xqQ_v0p6ko8STbRMHQ3CtJrBv_EBtg6_jpeq--Mvau_NojLSm-Zg2XqHAmxvWk5hExaL9uLOBPYuN1rh_pENs3DK5ZVHT7iGP05OMMP2jFdV5xhNuwBmpVRzwo0DGBKcaDAieR6hgK0NDggt8idTQxvuGr0qTdTwnFyDhMpB9PGB1ikfOvZZx2gyPphsfv7YSf1lrTqQY8vzI__J8nm1mq_liucw2m8UyW9wuEn7g-eJuPVtnd-tNtlmuVllcLwn_Nyh8mmUJh8HDj_FhDu_z5T_yHk5s)

```bash
# Search images from catalog
docker search ubuntu | head
```

Download an image from the remote registry.

```bash
# Download the ubuntu image
docker pull ubuntu:22.04
```

Open a [terminal](/terminals/docker)
and run an **interactive shell** (`--interactive`) with a terminal (`--tty`)
in a new container
based on `ubuntu:22.04`.
The `--rm` option removes the container when it exits.

**NB: run the following commands [in the terminal](/terminals/docker), not in the jupyter notebook**

```text
docker run --rm --tty --interactive ubuntu:22.04 /bin/bash
```

Now that you are on a "separate machine",
run the following commands in the new terminal
and ensure that you are on another "virtual host".

```text
# Operating System
cat /etc/issue
# Linux version
uname -a
```

---

#### Exercise

Now that you are in the [container's terminal](/terminals/docker),
what happens if you try to get the IP address using the following command?

```text
ip -4 -o a
```

Can you retrieve the container's IP address in another way?
**Hint: the `/proc` filesystem contains information about the system. Try to find the IP address in one of the files in `/proc`.**

---

## Dockerizing Applications

`busybox` is a lightweight Linux distribution.
You can run an one-shot command in a container.

```bash
docker run busybox /bin/echo 'Hello world'
```

---

## Docker commands

Here is a list of docker commands.

```text
docker create  # creates a container but does not start it.
docker run     # creates and starts a container.
docker stop    # stops it.
docker start   # will start it again.
docker restart # restarts a container.
docker rm      # deletes a container.
docker kill    # sends a SIGKILL to a container.
docker attach  # will connect to a running container.
docker wait    # blocks until container stops.
docker exec    # executes a command in a running container.
```

You can inspect containers

```text
docker ps      # shows running containers.
docker inspect # information on a container (incl. IP address).
docker logs    # gets logs from container.
docker events  # gets events from container.
docker port    # shows public facing port of container.
docker top     # shows running processes in container.
docker diff    # shows changed files in container's FS.
docker stats   # shows metrics, memory, cpu, filsystem
```

#### Exercise

1. List the running containers.

```python
# Use this cell to run the correct docker command.
```

1. Inspect the `ansible-101_bastion_1` container.
<!-- solution
docker inspect ansible-101_bastion_1
-->

1. Use the `--format` option to get the IP address on a [terminal](/terminals/docker).
   **Hint 1: you can google for the solution.**

<!-- solution
# In the bash terminal, or via %%bash
docker inspect ansible-101_bastion_1 --format '{{.Name}} {{.NetworkSettings.IPAddress}}'
-->

1. Try to run the above `docker inspect --format ...` command in the jupyter notebook.
   Does it work? If not, why?

<!-- solution
!docker inspect ansible-101_bastion_1 --format '{{{{.Name}}}} {{{{.NetworkSettings.IPAddress}}}}'
-->

```python
# Use this cell to run the correct docker command.
```

💬 Discuss how python treats the `{` character.

---

## Images

### Like VMs template images

Docker leverages a [copy-on-write filesystem](https://docs.docker.com/storage/storagedriver/).
This allows Docker to instantiate containers very quickly.
Docker layers one container filesytem on top of another.
For example, you might:

- create a container image from a base Debian image;
- then create another container based on the first image.

[![](https://mermaid.ink/img/pako:eNpVkstO6zAQhl_FmnVS2U7iNFmwQLBAiBVIR6I-QtPYoRaxXSW2RE_Vd8ckp7Ts5vLN7dccofNKQwvvI-530kk3xe1sk867gMbpcfNnNAG3g76EyIAHPf6VLnyGzcvOTEuAeDccztQkU3qnSW8GPZGww0Bw1MR6ZXqjVSrWTn1PvJppLL7rt7nX5sHauIyN2-hCbDlf0XJBSI9tj_ngu4_UZ4uTznl-Xdw0VVV0NSGMPt6eEfYLqRWvFWWE8OLpB6G_kJ6KAouCEEFn5P_CFxny_OZ65-8kZGD1aNGopOpROkIkJBmsltAmU-ke4xAkSHdKaNwrDPpemeBHaMMYdQYYg38-uO7sL8ydwaSRhXT3MKXoHt2r9_YMJRfaI3xCy8pyVdKqYrTkxbqhTQYHaHlTrUTViIILwfma1acM_s31dCVYxWnFxLrmJRWUZaDnhZ6W15g_5PQF27i6QA?type=png)](https://mermaid.live/edit#pako:eNpVkstO6zAQhl_FmnVS2U7iNFmwQLBAiBVIR6I-QtPYoRaxXSW2RE_Vd8ckp7Ts5vLN7dccofNKQwvvI-530kk3xe1sk867gMbpcfNnNAG3g76EyIAHPf6VLnyGzcvOTEuAeDccztQkU3qnSW8GPZGww0Bw1MR6ZXqjVSrWTn1PvJppLL7rt7nX5sHauIyN2-hCbDlf0XJBSI9tj_ngu4_UZ4uTznl-Xdw0VVV0NSGMPt6eEfYLqRWvFWWE8OLpB6G_kJ6KAouCEEFn5P_CFxny_OZ65-8kZGD1aNGopOpROkIkJBmsltAmU-ke4xAkSHdKaNwrDPpemeBHaMMYdQYYg38-uO7sL8ydwaSRhXT3MKXoHt2r9_YMJRfaI3xCy8pyVdKqYrTkxbqhTQYHaHlTrUTViIILwfma1acM_s31dCVYxWnFxLrmJRWUZaDnhZ6W15g_5PQF27i6QA)

---

This mechanism allows an efficient storage usage, since multiple containers can
reuse the same filesystem layers.

[![](https://mermaid.ink/img/pako:eNqlkk2P0zAQhv_KyAdOSRU7cb4OHBY4ILQnONEg5MaTrUVsV44ttnT733GTDaQSN-LL2HnmnZnXvpDeSiQteXLidOxMZ6ZwmGPorfFCGXR0_24NgcJPp7w4jAijOKP71hn_7On-y1FNywlYM57X5KmL_48IgxpxAn8UHoRD0FaqQaGM2Wjkv2qyTU22LcX-s9TdiEqLJ_w-a-0_ah2WwcIhGB9axnZZsSAwiHYQ6Wj7H1HnICZMWbpNbhrO874CoNmnhxWhd0glWSUzCsDyxz9IdocMWZmLPAcosxl5bfjvRcCbjUOQpm_hxaGQ6c2HOL7DMCHchNe2b168bMe86ZGEaHRaKBnv_dIZgI5E5zR2pI2hxEGE0XekM9eIhpMUHj9I5a0jrXcBEyKCt5_Ppl_3C_NeiWirJtGqcYqnJ2G-WqtXKG5JeyHPpKW83hWU5Tmva5ZzVrGEnEnLmnJX8qaseZ0XBY_rmpBfs0K249nyFVXDGOc0ITi39Lg83_kVX38DC_v2ew?type=png)](https://mermaid.live/edit#pako:eNqlkk2P0zAQhv_KyAdOSRU7cb4OHBY4ILQnONEg5MaTrUVsV44ttnT733GTDaQSN-LL2HnmnZnXvpDeSiQteXLidOxMZ6ZwmGPorfFCGXR0_24NgcJPp7w4jAijOKP71hn_7On-y1FNywlYM57X5KmL_48IgxpxAn8UHoRD0FaqQaGM2Wjkv2qyTU22LcX-s9TdiEqLJ_w-a-0_ah2WwcIhGB9axnZZsSAwiHYQ6Wj7H1HnICZMWbpNbhrO874CoNmnhxWhd0glWSUzCsDyxz9IdocMWZmLPAcosxl5bfjvRcCbjUOQpm_hxaGQ6c2HOL7DMCHchNe2b168bMe86ZGEaHRaKBnv_dIZgI5E5zR2pI2hxEGE0XekM9eIhpMUHj9I5a0jrXcBEyKCt5_Ppl_3C_NeiWirJtGqcYqnJ2G-WqtXKG5JeyHPpKW83hWU5Tmva5ZzVrGEnEnLmnJX8qaseZ0XBY_rmpBfs0K249nyFVXDGOc0ITi39Lg83_kVX38DC_v2ew)

----

## Commands for interacting with images

```text
docker images  # shows all images.
docker import  # creates an image from a tarball.
docker build   # creates image from Dockerfile.
docker commit  # creates image from a container.
docker rmi     # removes an image.
docker history # list changes of an image.
```

----

Images are stored in a Docker registry such as [Docker Hub](https://hub.docker.com/)
or Github's [Container Registry](https://ghcr.io/).
You can also host your own registry.

`docker commit` can create an image from a container:
this is the process used when building a `Dockerfile`.

NB. This is similar to the virtual machines' snapshot feature.

[![](https://mermaid.ink/img/pako:eNqtlV1vmzAUhv-K5WuIwDak4WIXXXcxbd3FVmnS4qpysEmsgImwUcu6_vc5diCQfkxre3fMeY3f8_jj3MO85gJmcN2w3QZcnVNFVV4yrS9EAVYlU1ugTVNvRaZqJYJClqWLRqr1ptbmoAo50xvWNKzLQDJWU6XblV9EVuubdtUq0y4_V1Vr2KoUwH_IEJpFxCrYWoCCZQULyzrfXlPFZSNyI2sFvn6nasW0CFHodDcl60SzXCySBOdzAOLoy_n1QRJPJHOO5jyKAUD4cpBEE0kRpZhhDEAaOYlQ_JF3JW6X38StjXvzL_rdM41Dc2eWVxupgVsH1KrsQF4rw6TSlCqzEaCquSyk4MBiE_p6sm4cekA3eb3r_gNbHDaiWIK-ktNyGrGWduO6U77HLfKxLXmYPJrO7SKiiZcffSG2LvSo9EGMQi71dvmzkd56PkzySLxvzmzW7svJfwBV6FUMnemRh9dhRE9gPKFARhTi5ymQN1Ig70CBvJICefIwPSKBRiTw8yTwG0ngdyCBJyT-eanxy7dpqEBbs_5q9AHqAzJMc28CCMMP08u9P2x7MC6DphlyzJBpBh8zeJo5GNmn_vjY-qwqaSyhvBHMCP2nf9bAYBeEM6tv9Sg5VHCa6x-KYaWn04eOAdyTFLgbFTiggTtXvtkcRaMiggmGYFJgMAHhexFVMICVaComuW1t91QBQKE9DpWgMLMhFwVrS0MhVQ9W2u7sKROfuDR1AzPTtCKArDX1j07l_dhrLiSzW11BeyZKbb_umPpV11UvskOY3cM7mKGEzNJFksYoTlCULlIcwA5mcURmhJAIz9P5GUJnCX4I4G_3h2g2X0QojhYpQvtWhlAAhbN06Tu0a9QPfwEgtsUC?type=png)](https://mermaid.live/edit#pako:eNqtlV1vmzAUhv-K5WuIwDak4WIXXXcxbd3FVmnS4qpysEmsgImwUcu6_vc5diCQfkxre3fMeY3f8_jj3MO85gJmcN2w3QZcnVNFVV4yrS9EAVYlU1ugTVNvRaZqJYJClqWLRqr1ptbmoAo50xvWNKzLQDJWU6XblV9EVuubdtUq0y4_V1Vr2KoUwH_IEJpFxCrYWoCCZQULyzrfXlPFZSNyI2sFvn6nasW0CFHodDcl60SzXCySBOdzAOLoy_n1QRJPJHOO5jyKAUD4cpBEE0kRpZhhDEAaOYlQ_JF3JW6X38StjXvzL_rdM41Dc2eWVxupgVsH1KrsQF4rw6TSlCqzEaCquSyk4MBiE_p6sm4cekA3eb3r_gNbHDaiWIK-ktNyGrGWduO6U77HLfKxLXmYPJrO7SKiiZcffSG2LvSo9EGMQi71dvmzkd56PkzySLxvzmzW7svJfwBV6FUMnemRh9dhRE9gPKFARhTi5ymQN1Ig70CBvJICefIwPSKBRiTw8yTwG0ngdyCBJyT-eanxy7dpqEBbs_5q9AHqAzJMc28CCMMP08u9P2x7MC6DphlyzJBpBh8zeJo5GNmn_vjY-qwqaSyhvBHMCP2nf9bAYBeEM6tv9Sg5VHCa6x-KYaWn04eOAdyTFLgbFTiggTtXvtkcRaMiggmGYFJgMAHhexFVMICVaComuW1t91QBQKE9DpWgMLMhFwVrS0MhVQ9W2u7sKROfuDR1AzPTtCKArDX1j07l_dhrLiSzW11BeyZKbb_umPpV11UvskOY3cM7mKGEzNJFksYoTlCULlIcwA5mcURmhJAIz9P5GUJnCX4I4G_3h2g2X0QojhYpQvtWhlAAhbN06Tu0a9QPfwEgtsUC)

---

## Building images with Dockerfile

The Dockerfile is a text file that contains all the commands a user could
call on the command line to assemble an image.

```bash
cat Dockerfile
```

Docker will execute all the commands in the Dockerfile and create a new image.

```bash
docker build -t apache-example .
```

Open the [terminal](/terminals/docker_1) and:

- inspect the image
- run the image with

```bash
docker run --rm --detach apache-example
```

#### Exercise

Open the [terminal](/terminals/docker_1) and:

- check if the container is running `docker ps`.
  Can you identify the container by its image name?
  What is the container's name?
- use `curl` to check if the webserver works.
  **Hint: you can retrieve the container IP using the previous command.**
<!-- solution

-->
- stop the container with `docker stop`
- check the container status with `docker ps -a`
- remove the container with `docker rm`

---

## docker-compose

[Docker Compose](https://docs.docker.com/compose/) is a tool for defining and running complex applications with
Docker.

With Compose, you define a multi-container application in a
single file, then spin your application up in a single command which
does everything that needs to be done to get it running.

----

## docker-compose

Using Compose is basically a three-step process:

1. define your app's image with a `Dockerfile`
1. define the services that make up your app in
   `docker-compose.yaml` so they can be run together in an isolated
environment.
1. run `docker-compose up` and Compose will start and run your
   entire app.

----

## docker-compose

docker-compose.yaml

```yaml
# This is a compose file defining a simple python
#   application with a redis database.
#
# Run with:
#
#  docker-compose up
version: '2'
services:
  web:
    build: .
    command: python app.py
    ports:
    - "5000:5000"
    volumes:
    - .:/code
    links:
    - redis
  redis:
    image: redis
```

Now run docker-compose up and Compose will start and run your entire app.

Docker Compose is a basic example of Infrastructure as Code.
The infrastructure setup is defined in a file, and can be versioned.
All the changes are tracked and can be reverted.
Administrators do not have to run commands on the server to setup the infrastructure.

```bash
docker-compose up -d
```

---

## docker-compose example

```yaml
version: "2"
services:
  web:
    image: piuma/phpsysinfo
    ports:
     - "80:80"
```

----

## docker-compose example

```yaml
version: "2"
services:
  web1:
    image: piuma/phpsysinfo
  web2:
    image: piuma/phpsysinfo
  proxy:
    image: tutum/haproxy
    links:
    - web1
    - web2
    ports:
    - "80:80"
```

----

## docker-compose example

```yaml
version: "2"
services:
  web1:
    image: piuma/phpsysinfo
  web2:
    image: piuma/phpsysinfo
  web3:
    image: piuma/phpsysinfo
  proxy:
    image: tutum/haproxy
    links:
    - web1
    - web2
    - web3
    ports:
    - "80:80"
```

----

## docker-compose example

```yaml
version: "2"
services:
  phpmyadmin:
    image: nazarpc/phpmyadmin
    links:
    - mysql
    ports:
    - "8080:80"
  mysql:
    image: mysql
    environment:
    - MYSQL_ROOT_PASSWORD=secret
```

---

## What next?

```bash
docker run --rm mribeiro/cowsay "Any questions?"
```

---
