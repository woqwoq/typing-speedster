from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Container, ScrollableContainer
from textual_plotext import PlotextPlot
from textual.app import App

class ResultsScreen(Screen):

    CSS_PATH='styles/ResultsScreen.css'

    resultsTitle = Static("Results", id="resultsTitle")

    mainPlot = PlotextPlot(id="mainPlot")

    infoLabelLeft = Static("asd", id="infoLabelLeft")
    infoLabelRight = Static("asd", id="infoLabelRight")
    infoLabelContainer = Container(infoLabelLeft, infoLabelRight, id="infoLabelContainer")

    textLabel = Static("asd", id="textLabel")
    textLabelContainer = ScrollableContainer(textLabel, id="textLabelContainer")

    wpm = 111
    cpm = 444
    accuracy_info = "100/0/150%"
    difficulty = "EASY"
    wordCount = 12
    time = "11 nov 2025"
    text = "hello\n\n wolrd lkja\nslkdj\nalksjd"

    def compose(self):
        yield self.resultsTitle
        yield self.mainPlot
        yield self.infoLabelContainer
        yield self.textLabelContainer


    def on_mount(self):
        text1 = '\n'.join([f"WPM:{str(round(self.wpm))}",
                    f"CPM:{str(round(self.cpm))}",
                    f"Accuracy:{self.accuracy_info}"])
        
        text2 = '\n'.join([f"Words:{self.wordCount}",
                        f"Difficulty:{self.difficulty}"])
        

        self.infoLabelContainer.border_title = f"Info"
        self.infoLabelContainer.border_subtitle = f"{self.time}"
        self.infoLabelContainer.styles.border_title_align = "center"
        self.infoLabelContainer.styles.border = ("heavy", "white")

        self.textLabelContainer.border_title = f"Text"
        self.textLabelContainer.styles.border_title_align = "center"
        self.textLabelContainer.styles.border = ("heavy", "white")

        self.textLabel.update(f"{self.text}")
        self.infoLabelLeft.update(text1)
        self.infoLabelRight.update(text2)



class TestApp(App):
    
    SCREENS={"Results" : ResultsScreen}

    BINDINGS = [("ctrl+f", "new_screen", "open new screen")]
    def compose(self):
        yield Static("asd")

    
    def action_new_screen(self):
        self.push_screen('Results')


TestApp().run()