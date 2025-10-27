from textual.widgets import Static
from textual.events import Key
from rich.text import Text
from rich.style import Style
from time import time

TEXT_STYLE = Style(color="white")
CURSOR_STYLE = Style(color="black", bgcolor="white")
DIM_TEXT_STYLE = Style(color="white", dim=True)
UNMATCH_TEXT_STYLE = Style(color="white", bgcolor="red")


class StaticKeyboardInput(Static):
    can_focus = True
    logger = open('logs/StaticKeyboardInput_LOG.ini', 'w')

    def __init__(self, placeholder: str = "", **kwargs):
        super().__init__(**kwargs)
        self.placeholder = placeholder
        self.text = ""
        self.cursor_pos = 0
        self.time_start = None
        self.time_end = None
        self.time_recent = None
        
    def on_mount(self):
        self.render_text()
        self.focus()


    #TODO: Make it more efficient using sets
    def highlight_mismatches(self, t: Text)->Text:
        for i in range(len(t)):
            if(t[i].plain != self.placeholder[i]):
                t.stylize(UNMATCH_TEXT_STYLE, i, i+1)

        return t

    def render_text(self):
        t = Text(self.text, TEXT_STYLE) +Text(self.placeholder[self.cursor_pos:], DIM_TEXT_STYLE)
        
        t = self.highlight_mismatches(t)

        if self.cursor_pos < len(t):
            t.stylize(CURSOR_STYLE, self.cursor_pos, self.cursor_pos + 1)
        else:
            t.append(" ", CURSOR_STYLE)

        self.update(t)

        self.check_start_stop()


    def on_key(self, event: Key):
        key = event.key

        if len(key) == 1 and key.isprintable():
            self.text = self.text[:self.cursor_pos] + key + self.text[self.cursor_pos:]
            self.cursor_pos += 1
        elif key == "space":
            self.text = self.text[:self.cursor_pos] + " " + self.text[self.cursor_pos:]
            self.cursor_pos += 1
        elif key == "backspace" and self.cursor_pos > 0:
            self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1

        self.render_text()


    def update_text(self, text: str):
        self.cursor_pos = 0
        self.text = ""
        self.placeholder = text
        self.time_start = None
        self.time_end = None
        self.render_text()

    def reset_text(self):
        self.update_text(self.text)

    def check_start_stop(self):
        logger = open('logs/Timer_LOG.ini', 'a+')
        if(self.cursor_pos == 1):
            self.time_start = time()

        if(self.cursor_pos-1 == len(self.placeholder)-1):
            self.time_end = time()
            
            self.time_recent = self.time_end - self.time_start
            logger.write(f"\n{self.text} - {self.time_recent} - { (len(self.text.split())/self.time_recent)*60 } WPM - { ((len(self.text)/4.7)/self.time_recent)*60 } WPM")
            self.reset_text()
