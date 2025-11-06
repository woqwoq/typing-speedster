from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Container, ScrollableContainer
from textual_plotext import PlotextPlot
from textual.app import App
from textual import log
from messages.TypingComplete import TypingCompleted

def calculate_wpm(text, time):
    return (len(text)/4.7/time)*60

def _calculate_raw_wpm(text, time):
    return max((len(text.split())/time)*60, ((len(text)/4.7)/time)*60)

class ResultsScreen(Screen):

    BINDINGS = [("ctrl+z", "close_screen", "Close")]
    CSS_PATH='styles/ResultsScreen.css'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, message: TypingCompleted):
        self.wpm = message.wpm
        self.cpm = message.cpm
        self.accuracy_info = message.accuracy_info
        self.difficulty = message.difficulty
        self.wordCount = message.wordCount
        self.time = message.time
        self.text = message.text
        self.timepoints = message.timepoints

    def compose(self):
        resultsTitle = Static("Results", id="resultsTitle")
        mainPlot = PlotextPlot(id="mainPlot")
        infoLabelLeft = Static("asd", id="infoLabelLeft")
        infoLabelRight = Static("asd", id="infoLabelRight")
        infoLabelContainer = Container(infoLabelLeft, infoLabelRight, id="infoLabelContainer")
        textLabel = Static("asd", id="textLabel")
        textLabelContainer = ScrollableContainer(textLabel, id="textLabelContainer")
        mistakesContainer = ScrollableContainer(id="mistakesContainer")
        
        yield resultsTitle
        yield mainPlot
        yield Container(infoLabelContainer, mistakesContainer, id="bigContainer")
        yield textLabelContainer
        yield Footer()

    def get_wpm_points(self):
        text = self.text[1:]
        wpm_points = []
        for i in range(len(self.timepoints)):
            wpm_points.append(calculate_wpm(text[:i], self.timepoints[i])) 
        return wpm_points
    
    def _render_plot(self):
        self.query_one("#mainPlot").plt.plot(self.get_wpm_points(), marker ="braille")

    def _update_labels(self):
        text1 = '\n'.join([f"WPM:{str(round(self.wpm))}",
            f"CPM:{str(round(self.cpm))}",
            f"Accuracy:{self.accuracy_info}"])
        
        text2 = '\n'.join([f"Words:{self.wordCount}",
                        f"Difficulty:{self.difficulty.name}"])


        self.query_one("#textLabel").update(f"{self.text}")
        self.query_one("#infoLabelLeft").update(text1)
        self.query_one("#infoLabelRight").update(text2)

    def _stylize(self):
        self.query_one("#mistakesContainer").border_title = f"Write something cool here"
        self.query_one("#mistakesContainer").styles.border_title_align = "center"
        self.query_one("#mistakesContainer").styles.border = ("heavy", "white")

        self.query_one("#infoLabelContainer").border_title = f"Info"
        self.query_one("#infoLabelContainer").border_subtitle = f"{self.time}"
        self.query_one("#infoLabelContainer").styles.border_title_align = "center"
        self.query_one("#infoLabelContainer").styles.border = ("heavy", "white")

        self.query_one("#textLabelContainer").border_title = f"Text"
        self.query_one("#textLabelContainer").styles.border_title_align = "center"
        self.query_one("#textLabelContainer").styles.border = ("heavy", "white")

    def on_mount(self):
        self._stylize()
        self._update_labels()
        self._render_plot()

        self.footer = Footer()
        self.mount(self.footer)

    def action_close_screen(self):
        self.app.pop_screen()
