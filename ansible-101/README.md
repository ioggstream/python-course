# Python for System Administrators

Browse this course with the [online notebook viewer!](http://nbviewer.jupyter.org/github/ioggstream/python-course/tree/master/python-for-sysadmin/notebooks/)

## Setup
See README.setup for detailed instruction on:

    - Linux
    - Windows
    - Mac OS

If you use docker, just run:

    # docker-compose up course
    # firefox http://localhost:8888

For ansible homework, setup the ssh keys and run:

    # docker-compose scale course=1 ansible=2

## Playing the course
An easy way to run the course is on Linux with:

    #pip install -r requirements.txt    # install dependencies
    #nosetests -v                       # check if everything is ok
    #jupyter-notebook notebooks/        # ;)

Each notebook is associated to a python file in scripts/.


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
 
