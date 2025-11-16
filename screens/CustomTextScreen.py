from textual.app import App, ComposeResult
from textual.widgets import TextArea, Static, Footer
from textual.binding import Binding
from textual.containers import Container
from textual import log

TextArea.BINDINGS = TextArea.BINDINGS[:-2]

class TextAreaSelection(App):

    CSS_PATH = "../styles/CustomTextScreen.css"

    BINDINGS =[
        Binding("ctrl+z", "save_text", "Save and Exit", priority=True)
    ]

    text_area = TextArea(placeholder="Type your custom text here...", id="textArea")
    text_stats = Static("a\nb\nc\na\nb\nc\na\nb\nc\n", id="textStats")


    def compose(self) -> ComposeResult:
        yield Container(self.text_area, Container(self.text_stats, id="textContainer"), id="container")
        yield Footer()

    def get_text_stats(self, text):
        word_count = len(text.split(' '))
        char_count = len(text)

        char_count = {}

        for char in text:
            if char in char_count:
                char_count[char] = char_count[char]+1
            else:
                char_count[char] = 1

    def action_save_text(self):
        log(self.text_area.text)
        



asd = TextAreaSelection()
asd.run()