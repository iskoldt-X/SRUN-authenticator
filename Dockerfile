FROM ubuntu:20.04
MAINTAINER iskoldt
RUN apt update \
	&& apt -y install python3-pip git \
	&& pip3 install requests \
	&& pip3 install netifaces \
	&& git clone https://github.com/iskoldt-X/SRUN-authenticator.git \
	&& cd /SRUN-authenticator \
	&& chmod +x srun_login.py
WORKDIR /SRUN-authenticator
ENV USERNAME admin
ENV PASSWORD password
ENV INTERFACES eth0
CMD ./srun_login.py
