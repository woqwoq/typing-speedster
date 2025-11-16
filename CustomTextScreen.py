from textual.app import App, ComposeResult
from textual.widgets import TextArea, Static, Footer
from textual.binding import Binding
from textual.containers import Container
from textual_plotext import PlotextPlot
from textual import log

from core.TextStats import TextStats

TextArea.BINDINGS = TextArea.BINDINGS[:-2]

class TextAreaSelection(App):

    CSS_PATH = "styles/CustomTextScreen.css"

    BINDINGS =[
        Binding("ctrl+z", "save_text", "Save and Exit", priority=True)
    ]

    text_area = TextArea(placeholder="Type your custom text here...", id="textArea")
    text_stats = Static("a\nb\nc\na\nb\nc\na\nb\nc\n", id="textStats")
    main_plot = PlotextPlot(id="mainPlot")

    stats = None


    def compose(self) -> ComposeResult:
        yield Container(self.text_area, Container(self.text_stats, self.main_plot, id="textContainer"), id="container")
        yield Footer()

    def get_text_stats(self):
        self.stats = TextStats(self.text_area.text)

    
    #  self.word_count = len(text.split(' '))
    #     self.char_count = len(text)

    #     self.vowels = {}
    #     self.consonants = {}
    #     self.symbols = {}

    def generate_stats_text(self):
        self.get_text_stats()
        return f"""Word Count: {self.stats.word_count}
Char Count: {self.stats.char_count}
Vowel Count: {self.stats.get_vowel_count()}
Consonant Count: {self.stats.get_consonant_count()}
Symbol Count: {self.stats.get_symbol_count()}"""
    
    def render_plot(self, data):
        self.query_one("#mainPlot").plt.plot(data, marker ="braille")

    def update_text_stats(self):
        self.text_stats.content = self.generate_stats_text()

    def action_save_text(self):
        # self.render
        log(self.text_area.text)
        self.update_text_stats()
        



asd = TextAreaSelection()
asd.run()