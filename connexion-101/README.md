# Mastering API Design at Scale

Design resilient, well-documented APIs that are easy to integrate!
Learn to use OpenAPI and JSON Schema in a contract-first approach to define data formats,
meaning and service behavior.
Apply HTTP standards for caching, throttling, and security,
building APIs that are predictable and robust.

## Abstract

In this workshop you will learn to design REST APIs that are
secure, resilient and well-documented, following web standars,
such as OpenAPI, HTTP and JSON-LD.

We'll adopt a contract-first approach to ensure clarity and consistency,
while also discussing when code-first tools like FastAPI can be safely used.

A methodological introduction will guide you in aligning business goals
with technical implementation using the “API Canvas”.

Finally, we'll explore strategies for maintaining consistency
across APIs in multi-organization ecosystems, including:

- enforcing API guidelines for service management and security.
- aligning schema semantics through schema registries and linked data principles.

## Agenda

10' Goals and Setup
15' Contract-First or Code-First?
15' API Canvas Design Metodology
15' Introducing OpenAPI, JSON Schema and service HTTP headers

break

15' Assisted API Design (with Spectral and <https://italia.github.io/api-oas-checker/>)
15' Secure schema modeling
10' Schema registries and semantics with JSON-LD
10' Adding API Semantics (with JSON-LD and Schema Editor)

break

15' API Semantics reprise
15' The importance of service management
10' Rate Limiting
10' Caching
10' Closing remarks

### Preparation

The workshop requires:

- internet connection
- access online tools that we'll use to design the API
- customizable python3 intepreter

Sources, docker-compose and further materials
will be available on github.com before the date.

We'll use [connexion](https://github.com/spec-first/connexion), a python framework which streamlines API creation.

## Local Setup

This course is based on Docker and Docker compose. As long as you have Docker
you can run it on any operating system.


```bash
git clone https://github.com/ioggstream/python-course.git
cd python-course/connexion-101
```


Docker should be exposed via TCP on 172.17.0.1:2375. If you have concerns
in exposing docker, just use a temporary VM for the course (see below).

On Linux, set

```
# vim /etc/systemd/system/multi-user.target.wants/docker.service
[Service]
...
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://172.17.0.1:2375
...
```

On Mac, check [the FAQ and this issue](https://github.com/docker/for-mac/issues/770#issuecomment-252560286)

Consider having enough bandwidth for the first run to download the images.

Run the environemnt with:

```bash
make course
```

And point the browser on the printed URL, eg.

```bash
xdg-open http://localhost:8888
```
