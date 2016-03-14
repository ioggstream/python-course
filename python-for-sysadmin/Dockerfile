#
# Docker image for ipython notebook and various
#  python courses
#
FROM python:2.7
MAINTAINER roberto.polli@par-tec.it

RUN apt-get -y update && apt-get -y install gcc make python-dev python-pip 
RUN apt-get -y update && apt-get -y install build-essential libblas-dev liblapack-dev gfortran  libfreetype6-dev libpng-dev
RUN apt-get -y clean


COPY requirements.txt /requirements.txt

# install requirements for both py2 and py3
RUN pip2 install -U pip
RUN pip2 install -r /requirements.txt
RUN pip install -r /requirements.txt

