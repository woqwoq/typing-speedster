from textual.message import Message

class AttemptEntryClicked(Message):
    def __init__(self, position_index: int):
        super().__init__()
        self.position_index = position_index