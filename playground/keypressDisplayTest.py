from textual.app import App

from widgets.KeypressDisplay import KeypressDisplay

class MyApp(App):
    def compose(self):
        yield KeypressDisplay("", id="keypressDisplay")


MyApp().run()