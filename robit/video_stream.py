import inspect
import rtcbot
import asyncio
from aiortc import RTCIceServer, RTCConfiguration
from typing import List, Union, Dict, Callable, Coroutine

try:
    import picamera
    camera = rtcbot.PiCamera(1920, 1088)
except (ImportError, ModuleNotFoundError):
    print("Falling back on CVCamera")
    camera = rtcbot.CVCamera(1920, 1080)


class VideoStream:
    def __init__(self, signalling_token: str, stun_servers: List[str] = None):
        self.signalling_url = f"wss://blokegaming.com/robitcontrol/webrtcsignal/{signalling_token}/"
        if stun_servers is None:
            self.stun_servers = [RTCIceServer("stun:stun.blokegaming.com")]

        self.closing = False

        self.i = 0

        self.ws_connected = False
        self.rtc_connected = False
        self.websocket_connect()
        self.rtc_setup()

    def rtc_setup(self):
        print("RTC setup")
        self.videoSubscription = camera.subscribe()
        self.connection = rtcbot.RTCConnection(rtcConfiguration=RTCConfiguration(self.stun_servers))
        self.connection._rtc.on('connectionstatechange', self.rtc_ready)
        self.connection.onError(self.rtc_error)
        self.connection.onClose(self.rtc_close)
        self.connection.video.putSubscription(self.videoSubscription)

    def websocket_connect(self):
        print("Websocket Connect")
        self.ws = rtcbot.Websocket(self.signalling_url)
        self.ws.onReady(self.websocket_ready)
        self.ws.onError(self.websocket_error)
        self.ws.onClose(self.websocket_close)
        self.ws.subscribe(self.websocket_message_handler)

    async def websocket_ready(self):
        if not self.ws_connected and self.ws.ready:
            print("RTC signalling websocket ready")
            self.ws.put_nowait({
                "type": "info",
                "message": "Robit Connected"
            })
            self.ws_connected = True

    async def websocket_error(self):
        print("RTC signalling websocket error")
        self.ws_connected = False
        if not self.closing and not self.rtc_connected:
            self.websocket_connect()

    async def websocket_close(self):
        print("RTC signalling websocket closed")
        self.ws_connected = False
        if not self.closing and not self.rtc_connected:
            self.websocket_connect()

    async def websocket_message_handler(self, message):
        handlers: Dict[str, Union[Coroutine, Callable]] = {
            "webrtc_offer": self.handle_offer,
            "info": self.handle_info,
            "heartbeat": None
        }
        handler = handlers.get(message['type'], print)
        if handler is None:
            return
        elif inspect.iscoroutinefunction(handler):
            asyncio.create_task(handler(message))
        else:
            handler(message)

    async def handle_offer(self, message):
        print("Offer received")
        remote_sdp = {"sdp": message["SDP"], "type": message["SDP_type"]}
        local_sdp = await self.connection.getLocalDescription(remote_sdp)
        self.ws.put_nowait({
            "type": "webrtc_answer",
            "SDP": local_sdp["sdp"],
            "SDP_type": local_sdp["type"]
        })
        print("Answer sent")
        await asyncio.sleep(10)
        if not self.rtc_connected:
            self.connection.close()

    async def handle_info(self, message):
        if message["message"] == "Peer Connected":
            self.ws.put_nowait({
                "type": "info",
                "message": "Robit Connected"
            })

    async def rtc_ready(self):
        if self.connection._rtc.connectionState == "connected":
            print("RTC ready")
            self.rtc_connected = True
            await self.ws.close()

    async def rtc_error(self, error):
        print("RTC connection error")

    async def rtc_close(self):
        print("RTC connection close")
        self.rtc_connected = False
        if not self.ws_connected and not self.closing:
            self.websocket_connect()
        if not self.closing:
            self.rtc_setup()

    def close(self):
        global camera
        self.closing = True
        camera.unsubscribe(self.videoSubscription)


if __name__ == "__main__":
    stream = VideoStream("test21")
    asyncio.get_event_loop().run_forever()
