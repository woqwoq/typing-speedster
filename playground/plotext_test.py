from textual import log
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

from textual.app import App, ComposeResult

from textual_plotext import PlotextPlot

class ScatterApp(App[None]):
    plot = PlotextPlot()

    def compose(self) -> ComposeResult:
        yield self.plot


    def get_wpm_points(self):
        wpm_points = []
        for i in range(len(data)):
            wpm_points.append(calculate_wpm(word[:i], data[i])) 
        return wpm_points

    def on_mount(self) -> None:
        self.query_one(PlotextPlot).styles.height = '50%'
        self.query_one(PlotextPlot).styles.background = 'red'
        plt = self.query_one(PlotextPlot).plt
        plt.plot(self.get_wpm_points(), marker ="braille")
        plt.title("Scatter Plot") # to apply a title

if __name__ == "__main__":
    ScatterApp().run()