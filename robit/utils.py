import asyncio
import concurrent.futures

loop = asyncio.get_event_loop()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)


def sync_to_async(func):
    async def wrapper(*args):
        return await loop.run_in_executor(executor, func, *args)
    return wrapper
