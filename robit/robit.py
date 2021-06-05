from .websocket import Websocket
from .updater import Updater
from .arduino import ArduinoConsumer
from .exceptions import ExitNicelyException
import asyncio


class Robit:
    def __init__(self, ws_url, key):
        self.ws = Websocket(ws_url, key)
        self.updater = Updater()
        self.ws.message_handler = self.consumer_handler
        self.arduino = ArduinoConsumer()

    async def consumer_handler(self, message):
        if message["type"] == "update":
            try:
                await self.updater.handle(message)
            except ExitNicelyException:
                await self.ws.disconnect()

    async def _run(self):
        asyncio.create_task(self.arduino.receive_messages())
        await self.arduino.handle({"command": "motors", "left": 10, "right": 10})
        await asyncio.sleep(1)
        await self.arduino.handle({"command": "motors", "left": 0, "right": 0})
        await self.ws.connect()
        # asyncio.create_task(self.ws.connect())

    def run(self):
        asyncio.get_event_loop().run_until_complete(self._run())
