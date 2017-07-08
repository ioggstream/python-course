FROM itscaro/debian-ssh:latest
RUN apt-get -y update && apt-get -y install python sshpass
RUN apt-get -y clean
RUN apt-get -y autoremove

RUN echo "UseDNS no" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

