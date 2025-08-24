# Home Assistant add-on base (arch is injected by the Supervisor)
ARG BUILD_FROM
FROM ${BUILD_FROM}
ENV LANG=C.UTF-8

RUN apk add --no-cache python3 py3-pip jq gcc musl-dev python3-dev \
 && python3 -m pip install --no-cache-dir --upgrade pip \
 && pip3 install --no-cache-dir zkaccess-c3 requests

COPY zkteco_ha_bridge.py /usr/local/bin/zkteco_ha_bridge.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh /usr/local/bin/zkteco_ha_bridge.py
CMD ["/run.sh"]
