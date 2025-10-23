#!/usr/bin/env python3
"""
Live network time display.

- Fetches the current time from worldtimeapi.org (based on your IP/region).
- Keeps a smoothly updated clock by advancing from a monotonic timer.
- Re-syncs from the internet every few minutes when online.
- Falls back to the local system clock until the network is back.

Requires: requests  (pip install requests)
"""

import time
from datetime import datetime, timedelta, timezone
import requests

API_URL = "https://worldtimeapi.org/api/ip"   # public, no auth
SYNC_EVERY_SEC = 300                          # re-sync interval (5 minutes)
TIMEOUT_SEC = 4                               # HTTP timeout

def get_network_time():
    """Return a timezone-aware datetime from the web (or raise)."""
    r = requests.get(API_URL, timeout=TIMEOUT_SEC)
    r.raise_for_status()
    data = r.json()

    # Example: "2025-03-15T12:34:56.789123+01:00"
    dt_iso = data["datetime"]
    # Python 3.11+: datetime.fromisoformat handles the Z/offset fully
    net_dt = datetime.fromisoformat(dt_iso)
    # Ensure tz-aware (worldtimeapi returns offset, so it is tz-aware)
    if net_dt.tzinfo is None:
        # Fallback: if tz missing, treat as UTC
        net_dt = net_dt.replace(tzinfo=timezone.utc)

    tz_name = data.get("timezone", "Unknown TZ")
    return net_dt, tz_name

def main():
    print("Fetching network time… (Ctrl+C to quit)")
    base_net_dt = None
    tz_name = "Local"
    base_mono = time.monotonic()
    last_sync = base_mono

    # Try initial network sync
    try:
        base_net_dt, tz_name = get_network_time()
        base_mono = time.monotonic()
        last_sync = base_mono
        print(f"✓ Synced with internet time ({tz_name}).")
    except Exception as e:
        print(f"⚠ Could not reach time server ({e}). Using system clock until online.")
        base_net_dt = datetime.now().astimezone()
        base_mono = time.monotonic()
        last_sync = base_mono

    try:
        while True:
            now_mono = time.monotonic()
            # Advance the clock from the last known network (or local) time
            elapsed = now_mono - base_mono
            current_dt = base_net_dt + timedelta(seconds=elapsed)

            # Periodic re-sync attempt
            if now_mono - last_sync >= SYNC_EVERY_SEC:
                try:
                    new_dt, tz_name = get_network_time()
                    base_net_dt = new_dt
                    base_mono = time.monotonic()
                    last_sync = base_mono
                except Exception:
                    # Keep running; try again next interval
                    last_sync = now_mono  # avoid tight retry loop

            # Pretty print in place
            display = current_dt.strftime("%Y-%m-%d %H:%M:%S")
            tz_disp = tz_name
            print(f"\r{display}  ({tz_disp})", end="", flush=True)
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nBye!")

if __name__ == "__main__":
    main()
