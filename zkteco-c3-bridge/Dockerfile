# Home Assistant add-on base (arch is injected by the Supervisor)
ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8

# Install Python & tools (single line avoids line-continuation issues)
RUN apk add --no-cache python3 py3-pip jq \
 && python3 -m pip install --no-cache-dir --upgrade pip \
 && pip3 install --no-cache-dir zkaccess-c3 requests

# Files
COPY zkteco_ha_bridge.py /usr/local/bin/zkteco_ha_bridge.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh /usr/local/bin/zkteco_ha_bridge.py

# Start
CMD ["/run.sh"]
