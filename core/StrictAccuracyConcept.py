def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def get_word_ranges(text):
    whitespaces = findOccurrences(text, ' ')
    if (len(whitespaces) == 0):
        n = len(text)
        if (n > 0): 
            return [[0, n-1]]

    word_ranges = []
    current_range = [0, whitespaces[0]-1]
    word_ranges.append(current_range)

    for i in range(len(whitespaces)-1):
        current_range = [whitespaces[i]+1, whitespaces[i+1]-1,]
        word_ranges.append(current_range)

    current_range = [whitespaces[-1]+1, len(text)-1]
    word_ranges.append(current_range)

    return word_ranges

def count_mismatched_words(word_ranges: list[list[int]], mismatches: dict):
    mistake_found_in = set()

    for mismatch in mismatches:
        for i in range(len(word_ranges)):
            if mismatch in range(word_ranges[i][0], word_ranges[i][1]+1):
                mistake_found_in.add(i)
                break

    return mistake_found_in

mismatches = {17, 5, 6, 13}
text = "true rest band boss"


ranges = get_word_ranges(text)
print(ranges)
print(count_mismatched_words(ranges, mismatches))