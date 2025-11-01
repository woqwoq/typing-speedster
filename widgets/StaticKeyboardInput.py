from textual.message import Message
from textual.widgets import Static
from textual.events import Key
from rich.text import Text
from rich.style import Style
from time import time

from textual import log


TEXT_STYLE = Style(color="white")
CURSOR_STYLE = Style(color="black", bgcolor="white")
DIM_TEXT_STYLE = Style(color="white", dim=True)
UNMATCH_TEXT_STYLE = Style(color="white", bgcolor="red")


class TypingCompleted(Message):
    def __init__(self, wpm: float, cpm: float, text: str):
        super().__init__()
        self.wpm = wpm
        self.cpm = cpm
        self.text = text


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
        
    def on_mount(self):
        self._render_text()
        self.focus()


    #TODO: Make it more efficient using sets
    #TODO: Replace unmatched char to what it should be
    def _highlight_mismatches(self, t: Text)->Text:
        for i in range(len(t)):
            if(t[i].plain != self.placeholder[i]):
                t.stylize(UNMATCH_TEXT_STYLE, i, i+1)

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
        # log(f"Typed Text:{list(self.text)}")
        # log(f"Cursor: {self.cursor_pos}")

        placeholder_text = list(self.placeholder)

        if(placeholder_text[self.cursor_pos] == '\n'):
            self.cursor_pos+=1
            self.text += '\n'

        # log(f"Typed Text:{list(self.text)}")
        # log(f"Cursor: {self.cursor_pos}")


    def on_key(self, event: Key):
        key = event.key

        if len(key) == 1 and key.isprintable():
            #Character can't be added if we're on a newline
            if(self.placeholder[self.cursor_pos] == '\n'):
                return
            
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

        self._render_text()

    def update_text(self, text: str):
        self.cursor_pos = 0
        self.text = ""
        self.placeholder = text
        self.time_start = None
        self.time_end = None
        self._render_text()

    def reset_text(self):
        self.update_text(self.placeholder)

    def _check_start_stop(self):
        if(self.cursor_pos == 1):
            self.time_start = time()

        if(self.cursor_pos-1 == len(self.placeholder)-1):
            self.time_end = time()
            
            #TODO: Add hit-ratio influence for the formulas
            self.time_recent = self.time_end - self.time_start
            wpm = max((len(self.text.split())/self.time_recent)*60, ((len(self.text)/4.7)/self.time_recent)*60)
            cpm = (len( list(self.text) )/self.time_recent)*60 

            self.post_message(TypingCompleted(wpm, cpm, self.text))
            self.reset_text()
