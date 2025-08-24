#!/usr/bin/env python3
import os, time, json, logging, requests
from datetime import datetime, timezone
from c3 import C3  # provided by zkaccess-c3 (pip)

LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOGLEVEL, logging.INFO))
log = logging.getLogger("zkteco-bridge")

PANEL_IP      = os.getenv("PANEL_IP", "10.1.1.201")
PANEL_PASS    = os.getenv("PANEL_PASS", "")
HA_URL        = os.getenv("HA_URL", "http://supervisor/core")
HA_TOKEN      = os.getenv("HA_TOKEN")  # provided by Supervisor
EVENT_TYPE    = os.getenv("EVENT_TYPE", "zkteco_card")
POLL_MS       = int(os.getenv("POLL_MS", "150"))

POST_TIMEOUT  = float(os.getenv("POST_TIMEOUT", "5.0"))
RECONNECT_SEC = int(os.getenv("RECONNECT_SEC", "5"))

def fire_event(payload: dict):
    # Supervisor-internal Core API path
    url = f"{HA_URL.rstrip('/')}/api/events/{EVENT_TYPE}"
    headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=payload, timeout=POST_TIMEOUT)
    r.raise_for_status()

def record_to_dict(rec):
    # Normalize fields across firmware variations
    d = {}
    for k in ("timestamp","time","event","event_code","card","cardno","card_no","door","reader","in_out"):
        if hasattr(rec, k):
            v = getattr(rec, k)
            if isinstance(v, (bytes, bytearray)):
                v = v.decode(errors="ignore")
            d[k] = v
    card = d.get("card") or d.get("cardno") or d.get("card_no")
    door = d.get("door")
    reader = d.get("reader")
    ts = d.get("timestamp") or d.get("time")

    return {
        "card": str(card) if card is not None else None,
        "door": door,
        "reader": reader,
        "event": d.get("event") or d.get("event_code"),
        "panel_ip": PANEL_IP,
        "panel_time": ts if ts else None,
        "received_at": datetime.now(timezone.utc).isoformat(),
        "raw": d,
        "source": "zkteco_bridge"
    }

def main():
    if not HA_TOKEN:
        raise SystemExit("Missing HA_TOKEN (Supervisor token)")

    while True:
        try:
            panel = C3(PANEL_IP)
            log.info("Connecting to panel %s ...", PANEL_IP)
            if not panel.connect(PANEL_PASS if PANEL_PASS else None):
                raise RuntimeError("Connect failed")
            log.info("Connected. Streaming RTLog...")
            while True:
                recs = panel.get_rt_log() or []
                for rec in recs:
                    payload = record_to_dict(rec)
                    # Only forward swipes that include a card number
                    if payload.get("card"):
                        fire_event(payload)
                        log.debug("Event -> HA: %s", json.dumps(payload))
                time.sleep(max(POLL_MS, 50) / 1000.0)
        except Exception as e:
            log.warning("Bridge error: %s (reconnecting in %ss)", e, RECONNECT_SEC)
            try:
                panel.disconnect()
            except Exception:
                pass
            time.sleep(RECONNECT_SEC)

if __name__ == "__main__":
    main()
