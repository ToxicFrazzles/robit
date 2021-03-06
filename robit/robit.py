from .websocket import Websocket
from .updater import Updater
from .arduino import ArduinoConsumer
from .exceptions import ExitNicelyException
from .video_stream import VideoStream
import asyncio


class Robit:
    def __init__(self, ws_url, key, rtc_signalling_token):
        self.ws = Websocket(ws_url, key)
        self.updater = Updater()
        self.ws.message_handler = self.consumer_handler
        self.arduino = ArduinoConsumer()
        self.video_stream = VideoStream(rtc_signalling_token, key)

    async def consumer_handler(self, message):
        if message["type"] == "update":
            try:
                await self.updater.handle(message)
            except ExitNicelyException:
                await self.ws.disconnect()
        elif message["type"] == "command":
            await self.arduino.handle(message)

    async def _run(self):
        asyncio.create_task(self.arduino.receive_messages())
        # Should turn right
        await self.arduino.handle({"command": "motors", "left": 100, "right": 0})
        await asyncio.sleep(1)
        await self.arduino.handle({"command": "motors", "left": 0, "right": 0})
        await asyncio.sleep(1)
        # Then left
        await self.arduino.handle({"command": "motors", "left": 0, "right": 100})
        await asyncio.sleep(1)
        await self.arduino.handle({"command": "motors", "left": 0, "right": 0})
        # await self.ws.connect()
        asyncio.create_task(self.ws.connect())

    def run(self):
        asyncio.get_event_loop().run_until_complete(self._run())
        asyncio.get_event_loop().run_forever()
