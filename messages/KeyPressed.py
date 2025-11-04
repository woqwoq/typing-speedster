from textual.message import Message
import time

class KeyPressed(Message):
    def __init__(self, key: str):
        super().__init__()
        self.key = key
        self.time = time.ctime(time.time())