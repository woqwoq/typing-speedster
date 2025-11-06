from enum import Enum

class Difficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    VERY_HARD = 3
    SELF_HARM = 4

    DEFAULT = 5

world_len_ranges = {
    0:[2 ,4],
    1: [2, 6],
    2: [4, 7],
    3: [6, 9],
    4: [8, 20]
}

order = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD, Difficulty.VERY_HARD, Difficulty.SELF_HARM]