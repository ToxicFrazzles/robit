import asyncio
import json
import websockets.client
import websockets.exceptions
from typing import Union


class Websocket:
    def __init__(self, ws_url, key):
        self.ws_url = ws_url
        self.key = key
        self.connection: Union[None, websockets.client.WebSocketClientProtocol] = None
        self.receiveTask = None
        self.heartbeatTask = None
        self.quitting = False
        self.message_handler = None

    async def connect(self):
        while not self.quitting:
            self.connection = await websockets.client.connect(self.ws_url)
            print("Control socket connected")
            self.receiveTask = asyncio.create_task(self.receiveMessage())
            self.heartbeatTask = asyncio.create_task(self.heartbeat())
            await self.authenticate()
            await self.connection.wait_closed()
            print("Control socket disconnected")

            if self.connection.close_code == 1008:
                print("Key is wrong length maybe?")
                self.quitting = True
            elif self.connection.close_code == 4001:
                print("Attempted to authenticate when already authenticated")
            elif self.connection.close_code == 4000:
                print("Key does not match the key for any robot")
                self.quitting = True
            elif self.connection.close_code == 4002:
                print("Attempted to send a message before authenticating")
            else:
                print("Unknown close code:", self.connection.close_code)

    async def authenticate(self):
        print("Authenticating with control socket")
        auth_payload = {
            "type": "auth",
            "key": self.key
        }
        await self.send(auth_payload)

    async def send(self, message_obj):
        message = json.dumps(message_obj)
        await self.connection.send(message)

    async def receiveMessage(self):
        try:
            async for message in self.connection:
                print(message)
                try:
                    message_obj = json.loads(message)
                except json.JSONDecodeError:
                    print("[JSON ERROR]:", message)
                    continue
                if self.message_handler is None:
                    print(message)
                else:
                    await self.message_handler(message_obj)
        except websockets.exceptions.ConnectionClosedError:
            pass

    async def heartbeat(self):
        while True:
            try:
                # print("Sending Heartbeat")
                await self.connection.send('{"type": "heartbeat"}')
                await asyncio.sleep(10)
            except websockets.exceptions.ConnectionClosed:
                # print("Closed")
                break

    async def disconnect(self):
        self.quitting = True
        await self.connection.close()
