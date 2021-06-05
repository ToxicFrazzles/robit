from typing import Dict


class BaseConsumer:
    def __init__(self):
        pass

    def handle(self, message: Dict):
        pass
