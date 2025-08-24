# ZKTeco C3 → Home Assistant Event Bridge (Add-on)

Streams ZKTeco C3/inBio RTLog card swipes to Home Assistant as a custom event (default: `zkteco_card`).

## How it works
- Connects to the panel (TCP 4370) and reads RTLog continuously.
- For each card swipe, fires a Home Assistant event via the Supervisor-provided Core API.
- No tokens to manage: uses the add-on's Supervisor token.

## Options
- `panel_ip` (string, required): IP of your panel (e.g., `10.1.1.201`)
- `panel_pass` (string, optional): panel communication password if set in ZKAccess
- `event_type` (string, default `zkteco_card`)
- `poll_interval_ms` (int, default `150`)
- `loglevel` (DEBUG|INFO|WARNING|ERROR)

## Listen & Automate
In Home Assistant → Developer Tools → Events → listen to `zkteco_card`.
Example automation:

```yaml
alias: ZKTeco — Log swipe
trigger:
  - platform: event
    event_type: zkteco_card
action:
  - service: logbook.log
    data:
      name: "C3 Swipe"
      message: >
        Card {{ trigger.event.data.card }} on door {{ trigger.event.data.door }}
        (reader {{ trigger.event.data.reader }}) event={{ trigger.event.data.event }}
mode: queued
```
