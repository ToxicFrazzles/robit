#!/usr/bin/env python3
from robit import Robit
import json
from pathlib import Path


this_dir = Path(__file__).parent


if __name__ == "__main__":
    with open(this_dir / "settings.json") as f:
        settings = json.load(f)
    url = settings.get("url", "wss://blokegaming.com/robitcontrol/robitsocket")
    key = settings["key"]
    rtc_signalling_url = settings["rtc_signalling_url"]
    robit = Robit(url, key, rtc_signalling_url)
    robit.run()
