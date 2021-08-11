#!/usr/bin/env python3
from robit import Robit
import json
from pathlib import Path
from generate_rtc_url import gen_token


this_dir = Path(__file__).parent


if __name__ == "__main__":
    with open(this_dir / "settings.json") as f:
        settings = json.load(f)
    url = settings.get("url", "wss://blokegaming.com/robitcontrol/robitsocket")
    key = settings.get("key", None)
    if key is None or key == "":
        print("The robot key needs setting")
    rtc_signalling_token = settings.get("rtc_signalling_token", None)

    if rtc_signalling_token is None or rtc_signalling_token == "":
        rtc_signalling_token = gen_token()
        settings["rtc_signalling_token"] = rtc_signalling_token
        with open(this_dir / "settings.json", "w") as f:
            json.dump(settings, f, indent=1)
        print("No webRTC signalling token was provided so one has been provided for you and saved.")
    print(f"Visit the following URL to view the stream: https://blokegaming.com/static/webrtc.html?t={rtc_signalling_token}")

    robit = Robit(url, key, rtc_signalling_token)
    robit.run()
