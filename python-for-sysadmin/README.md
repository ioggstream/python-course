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
- If you are a novice, consider reading the
   introductory crash course in ../python-basic/

- Introducing ipython
  - 01_ipython.ipy

- Managing files
  - 02_file_management.py

- Gathering system data
  - 01_system_data_gathering.py

- Introduction to nosetest
  - 02_nosetests_simple.py

- Parsing 101
  - 03_parsing_test.py
  - 03_parsing_benchmarks.py

- Data processing
  - 04_simple_processing.py
  - 04_logging_parsing.py

- Ansible
  - 05_ansible.py
