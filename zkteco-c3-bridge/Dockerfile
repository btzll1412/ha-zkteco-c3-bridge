# Home Assistant add-on base
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8

# System deps + Python deps
RUN apk add --no-cache python3 py3-pip jq \     && python3 -m pip install --no-cache-dir --upgrade pip \     && pip3 install --no-cache-dir zkaccess-c3 requests

# Files
COPY zkteco_ha_bridge.py /usr/local/bin/zkteco_ha_bridge.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh /usr/local/bin/zkteco_ha_bridge.py

# Start
CMD ["/run.sh"]
