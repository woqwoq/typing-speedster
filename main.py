from textual.app import App
from textual.widgets import Button, Label, Footer, Static, Collapsible, DataTable
from textual.containers import Container

from widgets.PersistentPlaceholderInput import PersistentPlaceholderInput
from widgets.PersistentPlaceholderTextArea import PersistentPlaceholderTextArea
from widgets.StaticKeyboardInput import StaticKeyboardInput, TypingCompleted
from widgets.AttemptSidebar import AttemptSidebar

from TextGenerator import TextGenerator

UNALLOWED_CHARS = {',', '.', "'", "-"}

class MyApp(App):
    
    BINDINGS =[
        ('ctrl+d', 'increase_words', 'Increase W CNT'),
        ('ctrl+a', 'decrease_words', 'Decrease W CNT'),
        ('ctrl+s', 'restart', 'Restart')
    ]

    CSS_PATH = "styles/styles.css"

    textGenerator = TextGenerator(123, "words.txt", UNALLOWED_CHARS)

    wordCount: int = 5

    textToType = textGenerator.get_text(wordCount)

    welcomeLabel = Label(id='welcomeLabel', content="Typing-Speedster")

    keyboardInput = StaticKeyboardInput(id='keyboardInput', placeholder=textToType)
    labels = Container( Label("15", id="timerLabel"), Label("", id="wpmLabel"), id="labelContainer")

    attemptSidebar = AttemptSidebar(id='attemptSidebarCollapsible', title='Previous Attempts')

    def compose(self):
        yield self.welcomeLabel
        yield self.labels
        yield self.keyboardInput
        yield self.attemptSidebar
        yield Footer()

    def on_mount(self):
        self.keyboardInput.border_title = f"{self.wordCount} Word Test"
        self.keyboardInput.border_subtitle = "Easy Difficulty"
        self.keyboardInput.styles.border_title_align = "center"
        self.keyboardInput.styles.border = ("heavy", "blue")

    def generate_new_text(self, amount: int):
        self.textToType = self.textGenerator.get_text(self.wordCount)

    def action_increase_words(self):
        self.wordCount+=1
        self.query_one('#keyboardInput').border_title = f"{self.wordCount} Word Test"
        self.generate_new_text(self.wordCount)
        self.keyboardInput.update_text(self.textToType)

    def action_decrease_words(self):
        self.wordCount-=1
        self.query_one('#keyboardInput').border_title = f"{self.wordCount} Word Test"
        self.generate_new_text(self.wordCount)
        self.keyboardInput.update_text(self.textToType)

    def action_restart(self):
        self.generate_new_text(self.wordCount)
        self.keyboardInput.update_text(self.textToType)

    async def on_typing_completed(self, message: TypingCompleted):
        self.query_one('#wpmLabel').update(f"{message.wpm:.0f} WPM {message.cpm:.0f} CPM")
        # self.query_one('#timerLabel').update(f"{message.cpm:.0f} CPM")



MyApp().run()