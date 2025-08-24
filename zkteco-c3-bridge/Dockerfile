# Supervisor injects the right base image for your arch
ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8

# System deps
RUN apk add --no-cache python3 py3-pip jq

# Isolated virtualenv (avoids PEP 668)
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# Python deps (install into the venv)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir zkaccess-c3 requests

# Files
COPY zkteco_ha_bridge.py /usr/local/bin/zkteco_ha_bridge.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh /usr/local/bin/zkteco_ha_bridge.py

CMD ["/run.sh"]
