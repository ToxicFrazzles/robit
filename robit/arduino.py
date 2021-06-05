from .base_consumer import BaseConsumer
from typing import Dict
import serial
from .utils import sync_to_async


@sync_to_async
def send_message(conn, data):
    return conn.write(data)


class ArduinoConsumer(BaseConsumer):
    def __init__(self):
        super().__init__()
        self.serial = serial.Serial("/dev/ttyUSB0", baudrate=9600)

    async def handle(self, message: Dict):
        print(message)
        if message["command"] == "motors":
            left = message["left"]
            right = message["right"]
            data = f"m{left},{right};".encode('utf-8')
            print(data)
            byte_count = await send_message(self.serial, data)
            if byte_count != len(data):
                print(f"Only sent {byte_count} out of {len(data)} bytes")
