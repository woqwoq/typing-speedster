from textual.app import App
from textual.widgets import Button, Label, Footer, Input

class MyApp(App):
    wordCount: int = 0

    BINDINGS =[
        ('ctrl+d', 'increase_words', 'Increase W CNT'),
        ('ctrl+a', 'decrease_words', 'Decrease W CNT')
    ]
    CSS_PATH = "styles.css"

    welcomeLabel = Label(id='welcomeLabel', content="Vlad's Typing-Speedster")
    keyboardInput = Input(id='keyboardInput', placeholder="tho this is not your name")
    restartButton = Button(id='restartButton', label="Restart")

    def compose(self):
        yield self.welcomeLabel
        yield self.restartButton
        yield self.keyboardInput
        yield Footer()

    def on_mount(self):
        self.keyboardInput.border_title = "10 Word Test"
        self.keyboardInput.border_subtitle = "Easy Difficulty"
        self.keyboardInput.styles.border_title_align = "center"

    def action_increase_words(self):
        self.wordCount+=1
        self.query_one('#keyboardInput').border_title = f"{self.wordCount} Word Test"

    def action_decrease_words(self):
        self.wordCount-=1
        self.query_one('#keyboardInput').border_title = f"{self.wordCount} Word Test"



MyApp().run()