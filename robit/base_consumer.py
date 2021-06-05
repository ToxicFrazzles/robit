from typing import Dict


class BaseConsumer:
    def __init__(self):
        pass

    async def handle(self, message: Dict):
        pass
