#
# This is a simple Dockerfile to build an image with Apache2.
# You can build it with:
#
#  $ docker build -t test-apache2 .
#
FROM docker.io/debian:bullseye

# Set the maintainer. See https://docs.docker.com/engine/reference/builder/#maintainer-deprecated
LABEL org.opencontainers.image.authors="piuma@piumalab.org"

# Install Apache2 and finally clean up the APT cache.
#   There are different opinions on whether to `apt-get -y upgrade` or not.
#   Check this interesting discussion: https://github.com/docker/docs/pull/12571
RUN apt-get update && apt-get -y install apache2 && apt-get clean

# Expose the default ports. https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 80/tcp
EXPOSE 443/tcp

# Set the default command to run when starting the container
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
