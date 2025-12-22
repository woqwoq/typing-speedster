import random
from core.modes.ModeAbstract import Mode

class TextMode(Mode):
    def __init__(self, seed: int, source_path: str, unallowed_chars: dict) -> None:

        self.recent_description = ""
        self.source_path = source_path
        self.seed = seed
        self.unallowed_chars = unallowed_chars

        self.words = self._get_unique_words_from_file()
        self.word_count = len(self.words)
    

    def _get_unique_words_from_file(self):
        unique_words = set()
        file = open(self.source_path)

        for line in file:
            for word in line.split():
                curr_word = word.lower()
                unique_words.add(curr_word)
        return list(unique_words)
    

    def _remove_unallowed_chars(self, text: str):
        for unallowed_char in self.unallowed_chars:
            text = text.replace(unallowed_char, '')
        
        return text
    
    def _get_error_text(self, path):
        return f"Error: {path} is empty or doesn't exist!"

    def generate_text(self, amount: int, allowedLen: list):
        text = []
        for i in range(amount):
            current_index = random.randint(0, self.word_count-1)
            while(not(len(self.words[current_index]) >= allowedLen[0] and len(self.words[current_index]) <= allowedLen[1])):
                current_index = random.randint(0, self.word_count-1)

            text.append(self.words[current_index])

        text = self._remove_unallowed_chars(' '.join(text))
        return text
    
