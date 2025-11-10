import random
from textual import log
from core.Mode import Mode

class TextGenerator():
    
    def __init__(self, seed: int, text_source_path: str, lyrics_source_path: str = None, quote_source_path: str = None, code_source_path: str = None, unallowed_chars: dict = {}):
        self.seed = seed
        self.text_source_path = text_source_path
        self.lyrics_source_path = lyrics_source_path
        self.quote_source_path = quote_source_path
        self.code_source_path = code_source_path

        self.words = self._get_unique_words_from_file()
        self.word_count = len(self.words)
        self.unallowed_chars = unallowed_chars
        random.seed(seed)


    def _get_unique_words_from_file(self):
        unique_words = set()
        file = open(self.text_source_path)

        for line in file:
            for word in line.split():
                curr_word = word.lower()
                unique_words.add(curr_word)
        return list(unique_words)
    

    def _remove_unallowed_chars(self, text: str):
        for unallowed_char in self.unallowed_chars:
            text = text.replace(unallowed_char, '')
        
        return text
    
    def generate_text(self, amount: int, allowedLen: list):
        text = []
        for i in range(amount):
            current_index = random.randint(0, self.word_count-1)
            while(not(len(self.words[current_index]) >= allowedLen[0] and len(self.words[current_index]) <= allowedLen[1])):
                current_index = random.randint(0, self.word_count-1)

            text.append(self.words[current_index])

        text = self._remove_unallowed_chars(' '.join(text))
        return text
    
    def generate_lyrics(self, amount: int):
        lyrics_lines = open(self.lyrics_source_path).readlines()
        start = random.randint(0, len(lyrics_lines)-amount-1)
        end = start+amount

        return ''.join(lyrics_lines[start:end])



    def get_text(self, mode: Mode, amount: int, allowedLen: list):
        match mode:
            case Mode.TEXT:
                return self.generate_text(amount, allowedLen)
            case Mode.LYRICS:
                return self.generate_lyrics(amount)
            # case Mode.QUOTE:
            #     self.generate_quote(amount)
            # case Mode.CODE:
            #     self.generate_code(amount)
