# Python Basic

This is a python crash course.

You can read it [here](http://nbviewer.ipython.org/github/ioggstream/python-course/tree/master/python-basic/notebooks/)
and use it:

    - via ipython
    - via ipython notebook


## Setup on Linux

Install the dependencies either with:

    - #pip install -r requirements.txt

    - #sudo apt-get install ipython-notebook

    - #sudo yum install ipython-notebook


## Setup with Docker Compose

If you have docker and compose you can just run (and wait for download):

    #docker-compose up


## Setup on Windows and Mac OS

Download python from [Continuum](http://continuum.io/downloads) and
install following the [provided instructions](http://docs.continuum.io/anaconda/install.html)

Then from the terminal:

    #conda update conda
    #conda update ipython ipython-notebook ipython-qtconsole \
        readline psutil matplotlib scipy numpy nose
