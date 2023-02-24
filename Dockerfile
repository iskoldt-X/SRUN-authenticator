FROM python:3.9-slim-bullseye AS build
COPY requirements.txt /requirements.txt
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc python3-dev libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel && \
    /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM python:3.9-slim-bullseye
MAINTAINER iskoldt
COPY --from=build /venv /venv
COPY ./srun_login.py /app/
WORKDIR /app
ENV USERNAME admin
ENV PASSWORD password
ENV INTERFACES eth0
ENV init_url https://portal.ucas.ac.cn
ENV get_challenge_api https://portal.ucas.ac.cn/cgi-bin/get_challenge
ENV srun_portal_api https://portal.ucas.ac.cn/cgi-bin/srun_portal
CMD ["/venv/bin/python3", "srun_login.py"]
