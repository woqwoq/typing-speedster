from textual.widgets import Static
from textual.events import Key
from rich.text import Text
from rich.style import Style

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
        
    def on_mount(self):
        self.render_text()


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
        self.render_text()
