#
# Docker image for ipython notebook and various
#  python courses
#
FROM docker.io/python:2.7
LABEL maintainer="roberto.polli@par-tec.it"

RUN ulimit -n 1024 && apt-get -y update && apt-get -y install gcc make python-dev python-pip
RUN ulimit -n 1024 && apt-get -y update && apt-get -y install build-essential libblas-dev liblapack-dev gfortran  libfreetype6-dev libpng-dev
RUN ulimit -n 1024 && apt-get -y update && apt-get -y install tree sshpass openssl
RUN ulimit -n 1024 && apt-get -y clean

RUN apt-get -y update && apt-get -y install curl apt-transport-https
RUN wget -O/root/foo.key https://download.docker.com/linux/debian/gpg && apt-key add /root/foo.key && rm /root/foo.key
RUN echo "deb [arch=amd64] https://download.docker.com/linux/debian buster stable" >> /etc/apt/sources.list
RUN apt-get -y update && apt-get -y install docker-ce
RUN apt-get -y clean

RUN apt-get -y autoremove

RUN pip2 install -U pip

COPY requirements.txt /requirements.txt

# install requirements for both py2 and py3
RUN pip2 install -r /requirements.txt
RUN pip install -r /requirements.txt

# Use folding extension
# RUN pip install jupyter_contrib_nbextensions
# RUN jupyter contrib nbextension install --user
# RUN jupyter nbextension enable codefolding/main
# RUN jupyter nbextension enable rubberband/main
# RUN jupyter nbextension enable exercise/main

# RUN jupyter nbextension install rise --py --sys-prefix
# RUN jupyter nbextension enable rise --py --sys-prefix
USER 1000
ENTRYPOINT /usr/local/bin/jupyter-notebook --ip 0.0.0.0
