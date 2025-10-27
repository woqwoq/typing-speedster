import random

class TextGenerator():
    
    def __init__(self, seed: int, source_path: str):
        self.seed = seed
        self.source_path = source_path
        self.words = self._get_unique_words_from_file()
        self.word_count = len(self.words)
        random.seed(seed)


    def _get_unique_words_from_file(self):
        unique_words = set()
        file = open(self.source_path)

        for line in file:
            for word in line.split():
                curr_word = word.lower()
                unique_words.add(curr_word)
        return list(unique_words)
    
    def get_text(self, amount: int):
        text = []
        for i in range(amount):
            current_index = random.randint(0, self.word_count-1)
            text.append(self.words[current_index])

        return ' '.join(text)
