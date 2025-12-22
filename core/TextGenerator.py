import random
from textual import log
from core.Mode import Mode
from core.JsonHandler import JsonHandler

from core.modes.TextMode import TextMode
from core.modes.LyricsMode import LyricsMode

JSON_CODE_SCHEMA = ['entry_desc', 'entry_text']
JSON_CODE_SCHEMA_PREPROCESS = [False, True]

JSON_LYRICS_SCHEMA = ['song_name', 'lyrics']
JSON_LYRICS_SCHEMA_PREPROCESS = [False, True]

class TextGenerator():
    
    def __init__(self, seed: int, text_source_path: str, lyrics_source_path: str = None, quote_source_path: str = None, code_source_path: str = None, unallowed_chars: dict = {}):
        self.seed = seed
        self.text_source_path = text_source_path
        self.lyrics_source_path = lyrics_source_path
        self.quote_source_path = quote_source_path
        self.code_source_path = code_source_path

        self.unallowed_chars = unallowed_chars
        
        self.recent_description = None
        
        random.seed(seed)

        
        self.text_mode = TextMode(seed, text_source_path, unallowed_chars)
        self.lyrics_mode = LyricsMode(seed, lyrics_source_path, unallowed_chars)

    def _get_error_text(self, path):
        return f"Error: {path} is empty or doesn't exist!"

    def generate_text(self, amount: int, allowedLen: list):
        text = self.text_mode.generate_text(amount, allowedLen)

        return text

    def generate_lyrics(self, song_number: int, allowedLen: list):
        text = self.lyrics_mode.generate_text(song_number, allowedLen)
        self.recent_description = self.lyrics_mode.recent_description

        return text

    def generate_code_fragment(self, number: int):
        handler = JsonHandler(self.code_source_path, JSON_CODE_SCHEMA, JSON_CODE_SCHEMA_PREPROCESS)
        if not handler.is_valid():
            return self._get_error_text(self.code_source_path)
        
        entry = handler.get_entry(number%handler.size())
        
        self.recent_description = entry[JSON_CODE_SCHEMA[0]]
        return ''.join(entry[JSON_CODE_SCHEMA[1]])

    def get_text(self, mode: Mode, amount: int, allowedLen: list):
        match mode:
            case Mode.TEXT:
                return self.generate_text(amount, allowedLen)
            case Mode.LYRICS:
                return self.generate_lyrics(amount, allowedLen)
            # case Mode.QUOTE:
            #     self.generate_quote(amount)
            case Mode.CODE:
                return self.generate_code_fragment(amount)
            case _:
                return self.generate_text(amount, allowedLen)
