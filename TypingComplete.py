from Difficulty import Difficulty
from textual.message import Message
import time

class TypingCompleted(Message):
    def __init__(self, wpm: float, cpm: float, text: str, difficulty: Difficulty, wordCount: int):
        super().__init__()
        self.wpm = wpm
        self.cpm = cpm
        self.text = text
        self.time = time.ctime(time.time())
        self.difficulty = difficulty
        self.wordCount = wordCount


    def generate_tooltip(self):
        return [f"WPM:{str(round(self.wpm))}",
                f"CPM:{str(round(self.cpm))}",
                f"Text:\"{self.text}\"",
                f"Date:{self.time}",
                f"Difficulty:{self.difficulty.name}",
                f"Words:{self.wordCount}"]