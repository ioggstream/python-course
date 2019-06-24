# Ansible 2 done right!


## Local Setup

This course is based on Docker and Docker compose. As long as you have Docker
you can run it on:

  - linux
  - mac
  - windows

Docker should be exposed via TCP on 172.17.0.1:2375

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

    # make course

or 

    # docker-compose scale course=1 bastion=1 web=3
    # firefox http://localhost:8888


## Playing the course on DigitalOcean

DigitalOcean is a great and cheap cloud-provider 

  - create an Ubuntu 16.04 docker droplet from the menu and ssh into your host
  - expose docker on local http port

```
# vim /etc/systemd/system/multi-user.target.wants/docker.service
[Service]
...
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://172.17.0.1:2375
...
```

  - clone and run the project

```
 # git clone https://github.com/ioggstream/python-course.git
 # cd python-course/ansible-101
 # make course


```

 - point to the reference url

See asciicast here

[![asciicast](https://asciinema.org/a/9xqX4akNND7Yc0Q1sTb3ZnEhI.png)](https://asciinema.org/a/9xqX4akNND7Yc0Q1sTb3ZnEhI)


## Outline


  - Ansible architecture
  - Describe delivery layout in ansible.cfg
  - Host and Group variables, Filters
  - Static and dynamic inventories (docker)
  - Vaults and Secrets
  - Use bastions and other ssh_opts
  - writing basic playbooks, test driven deployment
  - Yaml pitfalls
  - Inclusion and Roles
  - Ansible galaxy as a role repository (bonus track)
 
