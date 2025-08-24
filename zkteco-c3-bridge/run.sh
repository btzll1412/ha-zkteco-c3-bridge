#!/bin/sh
set -eu

# Read options (prefer bashio if present, else jq)
if [ -f /usr/lib/bashio/bashio.sh ]; then
  # shellcheck disable=SC1091
  . /usr/lib/bashio/bashio.sh
  PANEL_IP="$(bashio::config 'panel_ip')"
  PANEL_PASS="$(bashio::config 'panel_pass')"
  EVENT_TYPE="$(bashio::config 'event_type')"
  POLL_MS="$(bashio::config 'poll_interval_ms')"
  LOGLEVEL="$(bashio::config 'loglevel')"
else
  PANEL_IP="$(jq -r '.panel_ip' /data/options.json)"
  PANEL_PASS="$(jq -r '.panel_pass // ""' /data/options.json)"
  EVENT_TYPE="$(jq -r '.event_type' /data/options.json)"
  POLL_MS="$(jq -r '.poll_interval_ms' /data/options.json)"
  LOGLEVEL="$(jq -r '.loglevel' /data/options.json)"
fi

# Use Supervisor-injected token to call HA Core API
export HA_URL="http://supervisor/core"
export HA_TOKEN="${SUPERVISOR_TOKEN}"
export PANEL_IP PANEL_PASS EVENT_TYPE POLL_MS LOGLEVEL

echo "[zkteco-c3-bridge] panel_ip=${PANEL_IP}, event_type=${EVENT_TYPE}, poll=${POLL_MS}ms, loglevel=${LOGLEVEL}"

# Run with the venv’s Python
exec /opt/venv/bin/python /usr/local/bin/zkteco_ha_bridge.py
