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
    robit = Robit(url, key)
    robit.run()
