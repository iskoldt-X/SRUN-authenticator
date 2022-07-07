FROM debian:11-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc python3-dev libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel

FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM gcr.io/distroless/python3-debian11
MAINTAINER iskoldt
COPY --from=build-venv /venv /venv
COPY ./srun_login.py /app/
WORKDIR /app
ENV USERNAME admin
ENV PASSWORD password
ENV INTERFACES eth0
ENTRYPOINT ["/venv/bin/python3", "srun_login.py"]
#https://github.com/GoogleContainerTools/distroless/blob/main/examples/python3-requirements/Dockerfile
