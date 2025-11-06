from core.Difficulty import Difficulty
from textual.message import Message
import time

class TypingCompleted(Message):
    def __init__(self, wpm: float, cpm: float, text: str, difficulty: Difficulty, wordCount: int, accuracy_info: str, timepoints: list[float]):
        super().__init__()
        self.wpm = wpm
        self.cpm = cpm
        self.text = text
        self.time = time.ctime(time.time())
        self.difficulty = difficulty
        self.wordCount = wordCount
        self.accuracy_info = accuracy_info
        self.timepoints = timepoints


    def generate_tooltip(self):
        return [f"WPM:{str(round(self.wpm))}",
                f"CPM:{str(round(self.cpm))}",
                f"Accuracy:{self.accuracy_info}",
                f"Difficulty:{self.difficulty.name}",
                f"Words:{self.wordCount}",
                f"Date:{self.time}",
                f"Text:\"{self.text}\""]