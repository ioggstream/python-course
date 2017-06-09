# Ansible 2 done right!


## Setup

This course is based on Docker and Docker compose. As long as you have Docker
you can run it on:

  - linux
  - max
  - windows

Consider having enough bandwidth for the first run to download the images.


Run the environemnt with:

    # docker-compose scale course=1 ansible=3
    # firefox http://localhost:8888


## Playing the course
An easy way to run the course is on Linux with:

    #pip install -r requirements.txt    # install dependencies
    #nosetests -v                       # check if everything is ok
    #jupyter-notebook notebooks/        # ;)


## Outline


  - Ansible architecture
  - Describe delivery layout in ansible.cfg
  - Static and dynamic inventories (openstack / digitalocean example if internet connection available)
  - Vaults and Secrets
  - Use bastions and other ssh_opts
  - writing basic playbooks, test driven deployment
  - Yaml pitfalls
  - Group variables and roles
  - Ansible galaxy as a role repository
 
