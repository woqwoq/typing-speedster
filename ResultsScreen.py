from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Container, ScrollableContainer
from textual_plotext import PlotextPlot
from textual.app import App


word="the find ironrude  flag mom safe his bite tea"
data=[0.09623, 0.19995, 0.32818, 2.02798, 2.09321, 2.26131, 2.33726, 2.38723, 2.5194, 2.5853, 2.7284, 2.95142, 5.39564,
5.46967, 5.57683, 5.65851, 5.77244, 6.81476, 7.23391, 7.32829, 7.4136, 7.54837, 8.38022, 8.51546, 8.57685, 8.74353,
9.12128, 11.48832, 11.53899, 11.67891, 11.77251, 12.00076, 14.05912, 14.12718, 14.29532, 14.6036, 15.60142, 15.85549,
15.95795, 16.43433, 16.85646, 17.26867, 17.65022, 18.87732]

word = word[1:]
word_count = len(word)

#Need to dramatise drops more
def calculate_wpm(text, time):
    return (len(text)/4.7/time)*60


class ResultsScreen(Screen):

    CSS_PATH='styles/ResultsScreen.css'

    resultsTitle = Static("Results", id="resultsTitle")

    mainPlot = PlotextPlot(id="mainPlot")

    infoLabelLeft = Static("asd", id="infoLabelLeft")
    infoLabelRight = Static("asd", id="infoLabelRight")
    infoLabelContainer = Container(infoLabelLeft, infoLabelRight, id="infoLabelContainer")

    textLabel = Static("asd", id="textLabel")
    textLabelContainer = ScrollableContainer(textLabel, id="textLabelContainer")

    mistakesContainer = ScrollableContainer(id="mistakesContainer")

    wpm = 111
    cpm = 444
    accuracy_info = "100/0/150%"
    difficulty = "EASY"
    wordCount = 12
    time = "11 nov 2025 22:35 2025 asd"
    text = word

    def compose(self):
        yield self.resultsTitle
        yield self.mainPlot
        yield Container(self.infoLabelContainer, self.mistakesContainer, id="bigContainer")
        yield self.textLabelContainer


    def get_wpm_points(self):
        wpm_points = []
        for i in range(len(data)):
            wpm_points.append(calculate_wpm(word[:i], data[i])) 
        return wpm_points

    def on_mount(self):
        text1 = '\n'.join([f"WPM:{str(round(self.wpm))}",
                    f"CPM:{str(round(self.cpm))}",
                    f"Accuracy:{self.accuracy_info}"])
        
        text2 = '\n'.join([f"Words:{self.wordCount}",
                        f"Difficulty:{self.difficulty}"])
        


        self.mistakesContainer.border_title = f"Write something cool here"
        self.mistakesContainer.styles.border_title_align = "center"
        self.mistakesContainer.styles.border = ("heavy", "white")

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

        plt = self.query_one(PlotextPlot).plt
        plt.plot(self.get_wpm_points(), marker ="braille")



class TestApp(App):
    
    SCREENS={"Results" : ResultsScreen}

    BINDINGS = [("ctrl+f", "new_screen", "open new screen")]
    def compose(self):
        yield Static("asd")

    
    def action_new_screen(self):
        self.push_screen('Results')


TestApp().run()