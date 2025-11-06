from textual.widgets import Static
from textual import log

from messages.AttemptEntryClicked import AttemptEntryClicked

class AttemptEntry(Static):
    position_index = 0

    def set_position_index(self, num: int):
        self.position_index = num

    def on_click(self):
        self.post_message(AttemptEntryClicked(self.position_index))