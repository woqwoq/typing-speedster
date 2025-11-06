from textual.widgets import Static
from textual.events import Key
from textual import log

from rich.text import Text
from rich.style import Style

from time import time

from widgets.StaticKeyboardInput import DIM_TEXT_STYLE, UNMATCH_TEXT_STYLE

IGNORED_CHARS = {'\n', '\t', ' '}
DEFAULT_OFFSET = 2
DEFAULT_STYLE = DIM_TEXT_STYLE
HIGHLIGHT_STYLE = UNMATCH_TEXT_STYLE


#TODO: Add a primitive animation because of performance drops.
class KeypressDisplay(Static):

    DEFAULT_CSS ="""
    KeypressDisplay{
        width: auto;
    }
    """

    can_focus = False

    layout = "qwertyuiop\nasdfghjkl\nzxcvbnm"
    text: Text = Text(layout, DEFAULT_STYLE)
    index_map = {}

    def offset_text(self):
        res = ""
        text = list(self.text.plain)
        newline_ctr = 1

        for i in range(len(text)):
            if text[i] != '\n':
                res += text[i]+(' '*DEFAULT_OFFSET)
            else:
                res += '\n' + ((" "*DEFAULT_OFFSET)*newline_ctr)
                newline_ctr += 1
        
        self.text = Text(res, DEFAULT_STYLE)

    def generate_index_map(self):
        text = self.text.plain
        for i in range(len(text)):
            curr_item = text[i]
            if curr_item not in IGNORED_CHARS:
                self.index_map[curr_item] = i


    def highlight_key(self, key):
        if key not in self.index_map:
            return
        
        key_pos = self.index_map[key]
        start_time = time()
        duration = 0.5

        def fade():
            t = self.text
            alpha = max(0, 1 - (time() - start_time) / duration)
            blended_style = Style(bgcolor=f"rgb({int(255*alpha)}, 0, 0)")
            t.stylize(blended_style, key_pos, key_pos+1)
            self.update(t)
            if alpha > 0:
                self.set_timer(0.1, fade)

        fade()

    def on_key(self, event: Key):
        key = event.key.lower()

        if(key in self.index_map):
            self.highlight_key(key)
        
    def on_mount(self):
        self.offset_text()
        self.generate_index_map()
        self.update(self.text)