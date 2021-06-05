import os
import subprocess
from .base_consumer import BaseConsumer
from .utils import sync_to_async
from .exceptions import ExitNicelyException


def update():
    fqbn = "arduino:avr:nano"
    arduino_cli = "/home/pi/.local/bin/arduino-cli"
    res = subprocess.run(["git", "pull"], capture_output=True)
    if b"Already up-to-date" in res.stdout or b"Already up to date" in res.stdout:
        print("Already up-to-date")
        return False
    os.system(f"{arduino_cli} core update-index")
    os.system(f"{arduino_cli} compile --fqbn {fqbn} firmware")
    os.system(f"{arduino_cli} upload -p /dev/ttyUSB0 --fqbn {fqbn} firmware")
    return True


class Updater(BaseConsumer):
    def __init__(self):
        super().__init__()
        if update():
            exit(0)

    async def handle(self, message):
        print("Update notification")
        res = await sync_to_async(update)()
        if res:
            raise ExitNicelyException("An update has been downloaded")
        else:
            print("No update really. False alarm.")
