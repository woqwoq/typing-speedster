import random
from core.modes.ModeAbstract import Mode

from core.JsonHandler import JsonHandler

JSON_LYRICS_SCHEMA = ['song_name', 'lyrics']
JSON_LYRICS_SCHEMA_PREPROCESS = [False, True]

class LyricsMode(Mode):
    def __init__(self, seed: int, source_path: str, unallowed_chars: dict) -> None:

        self.recent_description = ""
        self.source_path = source_path
        self.seed = seed
        self.unallowed_chars = unallowed_chars

    def _get_error_text(self, path):
        return f"Error: {path} is empty or doesn't exist!"

    def generate_text(self, amount: int, allowedLen: list):
        song_number = amount
        handler = JsonHandler(self.source_path, JSON_LYRICS_SCHEMA, JSON_LYRICS_SCHEMA_PREPROCESS)
        if not handler.is_valid():
            return self._get_error_text(self.source_path)
        
        entry = handler.get_entry(song_number%handler.size())
        lyrics_lines = entry[JSON_LYRICS_SCHEMA[1]]

        line_count = random.randint(allowedLen[0], allowedLen[1])

        start = random.randint(0, len(lyrics_lines)-line_count-1)
        end = start+line_count

        self.recent_description = entry[JSON_LYRICS_SCHEMA[0]]
        return ''.join(lyrics_lines[start:end])
