import asyncio
from robit.utils import sync_to_async
import serial


@sync_to_async
def send_message(data):
    return conn.write(data)


async def main():
    await send_message(b"m50,50;")
    await asyncio.sleep(1)
    await send_message(b"m0,0;")


if __name__ == "__main__":
    conn = serial.Serial("/dev/ttyUSB0", 9600)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
