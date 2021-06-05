from .base_consumer import BaseConsumer
from typing import Dict


class ArduinoConsumer(BaseConsumer):
    def __init__(self):
        super().__init__()

    def handle(self, message: Dict):
        pass
