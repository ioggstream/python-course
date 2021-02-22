#
# Docker image for ipython notebook and various
#  python courses
#
FROM python:3.8
MAINTAINER roberto.polli@par-tec.it

RUN apt-get -y update && apt-get -y install gcc make python-dev python-pip 
RUN apt-get -y update && apt-get -y install build-essential libblas-dev liblapack-dev gfortran  libfreetype6-dev libpng-dev
RUN apt-get -y update && apt-get -y install tree sshpass openssl
RUN apt-get -y clean

RUN apt-get -y update && apt-get -y install curl apt-transport-https
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN echo "deb [arch=amd64] https://download.docker.com/linux/debian stretch stable" >> /etc/apt/sources.list
RUN apt-get -y update && apt-get -y install docker-ce
RUN apt-get -y clean

RUN apt-get -y autoremove

RUN pip3 install -U pip

COPY requirements.txt /requirements.txt

# install requirements for both py2 and py3
RUN pip2 install -r /requirements.txt
RUN pip install -r /requirements.txt

# Use folding extension
RUN pip install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --user
RUN jupyter nbextension enable codefolding/main
RUN jupyter nbextension enable rubberband/main
RUN jupyter nbextension enable exercise/main
RUN jupyter nbextension enable hide_input/main

RUN jupyter nbextension install rise --py --sys-prefix
RUN jupyter nbextension enable rise --py --sys-prefix

# Add API dependencies

COPY requirements-api.txt /requirements-api.txt
RUN pip3 install -r /requirements-api.txt

ENTRYPOINT /usr/local/bin/jupyter-notebook --ip 0.0.0.0
