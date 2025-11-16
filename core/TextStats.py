VOWELS = {'a', 'e', 'u', 'i', 'o'}
CONSONANTS = {
    'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
    'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'
}


class TextStats:
    def __init__(self, text):
        self.text = text

        self.word_count = len(text.split(' '))
        self.char_count = len(text)

        self.vowels = {}
        self.consonants = {}
        self.symbols = {}

        self._get_char_freq_dict()


    def _get_or_default(self, item, dict, default):
        if item not in dict:
            return default
        
        return dict[item]

    def _classify_letter(self, char):
        char = char.lower()
        if char in VOWELS:
            self.vowels[char] = self._get_or_default(char, self.vowels, 0)+1
        elif char in CONSONANTS:
            self.consonants[char] = self._get_or_default(char, self.consonants, 0)+1
        else:
            self.symbols[char] = self._get_or_default(char, self.symbols, 0)+1

    def _get_char_freq_dict(self):
        for char in self.text:
            self._classify_letter(char)

    def _update_stats(self):
        self.word_count = len(self.text.split(' '))
        self.char_count = len(self.text)

        self.vowels = {}
        self.consonants = {}
        self.symbols = {}

        self._get_char_freq_dict()

    def _count_dict_vals(self, dict):
        ctr = 0

        for val in dict:
            ctr += dict[val]

        return ctr

    def get_vowel_count(self):
        return self._count_dict_vals(self.vowels)
    
    def get_consonant_count(self):
        return self._count_dict_vals(self.consonants)
    
    def get_symbol_count(self):
        return self._count_dict_vals(self.symbols)

    def update_text(self, new_text):
        self.text = new_text

    
asd = TextStats("Hello, my name is vlad, im a second year comp sci student")

print(asd.word_count)
print(asd.char_count)
print(asd.vowels)
print(asd.consonants)
print(asd.symbols)
print(asd.get_vowel_count())
print(asd.get_consonant_count())
print(asd.get_symbol_count())