#!/usr/bin/env python3
import asyncio
import concurrent.futures
from pathlib import Path
import os
import websockets.client
import websockets.exceptions

this_dir = Path(__file__).parent.resolve()


def update():
    os.system(f"cd {this_dir}")
    os.system(f"git pull")


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
    updater = Updater()
    asyncio.get_event_loop().run_until_complete(updater.connect())
