#
# Docker image for ipython notebook and various
#  python courses
#
FROM centos:8

RUN dnf install -y  python36
RUN pip3 install jupyter



# Use folding extension
RUN pip3 install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --user
RUN jupyter nbextension enable codefolding/main
RUN jupyter nbextension enable rubberband/main
RUN jupyter nbextension enable exercise/main

# RUN jupyter nbextension install rise --py --sys-prefix
# RUN jupyter nbextension enable rise --py --sys-prefix

COPY config.json /root/.jupyter/jupyter_notebook_config.json

EXPOSE 8001

RUN dnf install -y curl
RUN dnf install -y curl dnf-plugins-core
RUN dnf config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
RUN dnf install -y docker-ce-cli

RUN curl >/etc/profile.d/99-docker.sh https://gist.githubusercontent.com/ioggstream/cc7caffc8e038ac27a9390a80c8e7cc0/raw/5fd6e39141631ea9e196d31dcf01e4ccddae376f/z99-docker-profile.sh
ENV DOCKER_HOST=tcp://172.17.0.1:2375
ENTRYPOINT jupyter notebook --ip 0.0.0.0 --port 8001 --allow-root

