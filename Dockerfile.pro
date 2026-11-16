FROM python:3.11-slim-bookworm AS build
# Build tools only for building wheels
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel && \
    /venv/bin/pip install --no-cache-dir -r /requirements.txt

FROM python:3.11-slim-bookworm
LABEL maintainer="iskoldt-X"
LABEL description="Torvalds-tier SRUN Authenticator"

# Set up a non-root user for security
RUN groupadd -r srun && useradd -r -g srun srun
WORKDIR /app
RUN chown srun:srun /app

# Copy virtualenv and application code
COPY --from=build /venv /venv
COPY --chown=srun:srun ./srun_login_pro.py /app/srun_login.py

USER srun
ENV PATH="/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Defaults (UCAS)
ENV SLEEP_TIME=300
ENV GET_IP_API="http://124.16.81.61/cgi-bin/rad_user_info?callback=JQuery"
ENV GET_CHALLENGE_API="https://portal.ucas.ac.cn/cgi-bin/get_challenge"
ENV SRUN_PORTAL_API="https://portal.ucas.ac.cn/cgi-bin/srun_portal"

CMD ["python", "srun_login.py"]
