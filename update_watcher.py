#!/usr/bin/env python3
import asyncio
import concurrent.futures
from pathlib import Path
import os
import subprocess
import websockets.client
import websockets.exceptions

this_dir = Path(__file__).parent.resolve()


def update():
    fqbn = "arduino:avr:nano"
    arduino_cli = "/home/pi/.local/bin/arduino-cli"
    res = subprocess.run(["git", "pull"], capture_output=True)
    if b"Already up-to-date" in res.stdout or b"Already up to date" in res.stdout:
        print("Already up-to-date")
        return
    os.system(f"{arduino_cli} core update-index")
    os.system(f"{arduino_cli} compile --fqbn {fqbn} firmware")
    os.system(f"{arduino_cli} upload -p /dev/ttyUSB0 --fqbn {fqbn} firmware")


class Updater:
    def __init__(self):
        self.connection = None
        self.uri = "wss://blokegaming.com/whs/sockets/h85hX5pLFlfBOKfquSS5cujMOFt1J8UWIfY0HYOS9JkIuENs0rUoPKUUDkotvVbb"
        self.receiveTask = None
        self.heartbeatTask = None
        self.quitting = False

    async def connect(self):
        while not self.quitting:
            self.connection = await websockets.client.connect(self.uri)
            self.receiveTask = asyncio.create_task(self.receiveMessage())
            self.heartbeatTask = asyncio.create_task(self.heartbeat())
            await self.connection.wait_closed()

    async def receiveMessage(self):
        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        async for message in self.connection:
            print("A push event has occurred on GitHub")
            await loop.run_in_executor(executor, update)
            self.quitting = True
            await self.connection.close()

    async def heartbeat(self):
        while True:
            try:
                await self.connection.send('ping')
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                break


if __name__ == "__main__":
    update()        # First make sure there hasn't been an update since the script last ran
    updater = Updater()
    asyncio.get_event_loop().run_until_complete(updater.connect())      # Update when the repo receives a push
