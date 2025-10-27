from textual.app import App
from textual.widgets import Button, Label, Footer, TextArea, Input
from textual.suggester import SuggestFromList
from widgets.PersistentPlaceholderInput import PersistentPlaceholderInput
from widgets.PersistentPlaceholderTextArea import PersistentPlaceholderTextArea


class MyApp(App):
    wordCount: int = 0

    BINDINGS =[
        ('ctrl+d', 'increase_words', 'Increase W CNT'),
        ('ctrl+a', 'decrease_words', 'Decrease W CNT')
    ]
    CSS_PATH = "styles/styles.css"

    textToType="if not self.text and self.placeholder:placeholder_lines = Content.from_text(self.placeholder).wrap(self.content_size.width)if y < len(placeholder_lines):"

    welcomeLabel = Label(id='welcomeLabel', content="Typing-Speedster")
    keyboardInput = PersistentPlaceholderTextArea(id='keyboardInput', placeholder=textToType)
    restartButton = Button(id='restartButton', label="Restart")

    attemptSidebar = Label(id='attemptSidebar', content="111WPM 20:35")

    def compose(self):
        yield self.welcomeLabel
        yield self.restartButton
        yield self.keyboardInput
        yield self.attemptSidebar
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