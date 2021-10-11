#
# Docker image for ipython notebook and various
#  python courses
#
FROM ipython/scipyserver
MAINTAINER roberto.polli@par-tec.it

COPY requirements.txt /requirements.txt

# install requirements for both py2 and py3
RUN pip2 install -r /requirements.txt
RUN pip install -r /requirements.txt
