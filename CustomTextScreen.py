from textual.app import App, ComposeResult
from textual.widgets import TextArea, Static, Footer
from textual.binding import Binding
from textual.containers import Container
from textual_plotext import PlotextPlot
from textual import log

from core.TextStats import TextStats, merge_arr

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

    def generate_stats_text(self):
        self.get_text_stats()
        return f"""Word Count: {self.stats.word_count}
Char Count: {self.stats.char_count}
Vowel Count: {self.stats.get_vowel_count()}
Consonant Count: {self.stats.get_consonant_count()}
Symbol Count: {self.stats.get_symbol_count()}"""
    
    def render_plot(self, x_data, y_data):
        self.main_plot.plt.clear_figure()
        self.main_plot.refresh()
        self.main_plot.plt.ylim(0, max(y_data))
        self.query_one("#mainPlot").plt.bar(x_data, y_data, marker ="braille", orientation="horizontal")

    def update_text_stats(self):
        self.text_stats.content = self.generate_stats_text()

    def action_save_text(self):
        self.update_text_stats()
        self.render_plot(merge_arr(self.stats.get_all_vowels(), self.stats.get_all_cons()), merge_arr(self.stats.get_all_vowel_freq(), self.stats.get_all_cons_freq()))
        
        
asd = TextAreaSelection()
asd.run()