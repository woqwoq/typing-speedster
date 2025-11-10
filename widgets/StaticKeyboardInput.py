from textual.widgets import Static
from textual.events import Key
from rich.text import Text
from rich.style import Style

from core.Difficulty import Difficulty
from messages.TypingComplete import TypingCompleted
from messages.KeyPressed import KeyPressed
from core.Utils import remove_if_greater

import time

from textual import log

SPECIAL_CHARACTER_MAP ={"number_sign"           : "#",
                        "less_than_sign"        : "<",
                        "greater_than_sign"     : ">",
                        "full_stop"             : ".",
                        "left_parenthesis"      : "(",
                        "right_parenthesis"     : ")",
                        "apostrophe"            : "'",
                        "left_curly_bracket"    : "{",
                        "right_curly_bracket"   : "]",
                        "left_square_bracket"   : "[",
                        "right_square_bracket"  : "]",
                        "quotation_mark"        : "\"",
                        "semicolon"             : ";",
                        "colon"                 : ":",
                        "tab"                   : "\t",
                        "minus"                 : "-",
                        "plus"                  : "+",
                        "equals_sign"           : "=",
                        "comma"                 : ",",
                        "question_mark"         : "?"}


TEXT_STYLE = Style(color="white")
CURSOR_STYLE = Style(color="black", bgcolor="white")
DIM_TEXT_STYLE = Style(color="white", dim=True)
UNMATCH_TEXT_STYLE = Style(color="white", bgcolor="red")


#TODO: Encapsulate keyboard input from high-level typing-test functionality
class StaticKeyboardInput(Static):
    can_focus = True

    def __init__(self, placeholder: str = "", **kwargs):
        super().__init__(**kwargs)

        self.placeholder = placeholder
        self.text = ""
        self.cursor_pos = 0

        self.time_start = None
        self.time_end = None
        self.time_recent = None

        self.mismatches = set()

        self.timepoints = []

        self.difficulty = Difficulty.DEFAULT #TODO: Fix the default difficulty to app's default difficulty
        self.wordCount = len(placeholder.split())
        
    def on_mount(self):
        self._render_text()
        self.focus()


    #TODO: Replace unmatched char to what it should be
    def _highlight_mismatches(self, t: Text)->Text:
        if self.cursor_pos == 0:
            return t
        
        #At this point cursor is one position in front of a typed character
        current_cursor = self.cursor_pos-1
        
        
        if(t[current_cursor].plain != self.placeholder[current_cursor]):
            self.mismatches.add(current_cursor)
            t.stylize(UNMATCH_TEXT_STYLE, current_cursor, current_cursor+1)
        elif current_cursor in self.mismatches:
            self.mismatches.remove(current_cursor)

        #Remove mismatches if a cursor has moved back
        self.mismatches = remove_if_greater(self.mismatches, current_cursor)

        #Highlight old mismatches
        for mismatch_index in self.mismatches:
            t.stylize(UNMATCH_TEXT_STYLE, mismatch_index, mismatch_index+1)

        return t

    def _render_text(self):
        t = Text(self.text, TEXT_STYLE) +Text(self.placeholder[self.cursor_pos:], DIM_TEXT_STYLE)
        t = self._highlight_mismatches(t)

        if self.cursor_pos < len(t):
            t.stylize(CURSOR_STYLE, self.cursor_pos, self.cursor_pos + 1)
        else:
            t.append(" ", CURSOR_STYLE)

        self.update(t)
        self._check_start_stop()


    #TODO: Fix cursor not displaying on newline char
    def _jump_to_new_line(self):
        placeholder_text = list(self.placeholder)

        if(placeholder_text[self.cursor_pos] == '\n'):
            self.cursor_pos+=1
            self.text += '\n'

    def on_key(self, event: Key):
        key = event.key
        if len(key) == 1 and key.isprintable():
            #Character can't be added if we're on a newline
            if(self.placeholder[self.cursor_pos] == '\n'):
                return
            
            self.post_message(KeyPressed(key))

            self.text = self.text[:self.cursor_pos] + key + self.text[self.cursor_pos:]
            self.cursor_pos += 1
        elif key == 'enter': 
            #Jump to the character after newline to continue
            self._jump_to_new_line()
        elif key == "space":
            #Character can't be added if we're on a newline
            if(self.placeholder[self.cursor_pos] == '\n'):
                return

            self.text = self.text[:self.cursor_pos] + ' ' + self.text[self.cursor_pos:]
            self.cursor_pos += 1
        elif key == "backspace" and self.cursor_pos > 0:
            self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1
        elif key in SPECIAL_CHARACTER_MAP:
            if(self.placeholder[self.cursor_pos] == '\n'):
                return
            
            if(key == 'tab'):
                event.stop()
            
            self.text = self.text[:self.cursor_pos] + SPECIAL_CHARACTER_MAP[key] + self.text[self.cursor_pos:]
            self.cursor_pos += 1


        self._render_text()

    def update_text(self, new_text: str, difficulty):
        self.wordCount = len(new_text.split())
        self.difficulty = difficulty

        self.cursor_pos = 0
        self.text = ""
        self.placeholder = new_text

        self.time_start = None
        self.time_end = None
        self.timepoints = []

        self._render_text()

    def reset_text(self):
        self.update_text(self.placeholder, self.difficulty)

    def _calculate_accuracy(self):
        return 1-len(self.mismatches)/len(self.text)

    def _calculate_raw_wpm(self):
        return max((len(self.text.split())/self.time_recent)*60, ((len(self.text)/4.7)/self.time_recent)*60)
    
    def _calculate_raw_cpm(self):
        return (len( list(self.text) )/self.time_recent)*60 

    def _check_start_stop(self):
        if(self.cursor_pos > 1 and self.cursor_pos-1 < len(self.placeholder)):
            self.timepoints.append(round(time.time() - self.time_start, 3))
            # log(f"word=\"{self.text}\"\ndata={self.timepoints}")
        if(self.cursor_pos == 1):
            self.time_start = time.time()

        if(self.cursor_pos-1 == len(self.placeholder)-1):
            self.time_end = time.time()
            
            #TODO: Add hit-ratio influence for the formulas
            self.time_recent = self.time_end - self.time_start

            wpm = self._calculate_raw_wpm()
            cpm = self._calculate_raw_cpm()

            accuraacy_info = f"{len(self.mismatches)}/{len(self.text)}/{round(self._calculate_accuracy()*100)}%"

            self.post_message(TypingCompleted(wpm, cpm, self.placeholder, self.difficulty, self.wordCount, accuraacy_info, self.timepoints))
            self.reset_text()
