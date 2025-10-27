from textual.app import App
from textual.widgets import Button, Label, Footer, TextArea, Static
from textual.suggester import SuggestFromList
from widgets.PersistentPlaceholderInput import PersistentPlaceholderInput
from widgets.PersistentPlaceholderTextArea import PersistentPlaceholderTextArea
from widgets.StaticKeyboardInput import StaticKeyboardInput


class MyApp(App):
    wordCount: int = 0

    BINDINGS =[
        ('ctrl+d', 'increase_words', 'Increase W CNT'),
        ('ctrl+a', 'decrease_words', 'Decrease W CNT')
    ]
    CSS_PATH = "styles/styles.css"

    textToType="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

    welcomeLabel = Label(id='welcomeLabel', content="Typing-Speedster")
    keyboardInput = StaticKeyboardInput(id='labelInput', placeholder=textToType)
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