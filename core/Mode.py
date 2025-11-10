from enum import Enum

class Mode(Enum):
    TEXT=0
    LYRICS=1
    CODE=2
    QUOTE=3

mode_order = [Mode.TEXT, Mode.LYRICS, Mode.CODE, Mode.QUOTE]