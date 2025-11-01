from textual.app import App
from textual.containers import Container
from textual.widgets import Label, Footer

from widgets.AttemptSidebar import AttemptSidebar
from widgets.StaticKeyboardInput import StaticKeyboardInput, TypingCompleted

from textual import log

from Difficulty import Difficulty, order, world_len_ranges

from TextGenerator import TextGenerator


UNALLOWED_CHARS = {',', '.', "'", "-"}

DEFAULT_DIFFICULTY = Difficulty.EASY
DEFUALT_WORD_COUNT = 5
DEFAULT_CSS_PATH = "styles/styles.css"
DEFAULT_TEXT_GENERATOR_SEED = 123
DEFUALT_WORD_DICTIONARY_PATH = "The_Oxford_3000.txt"

class MyApp(App):
    
    BINDINGS =[
        ('ctrl+d', 'increase_words', 'WORDS+'),
        ('ctrl+a', 'decrease_words', 'WORDS-'),
        ('ctrl+w', 'increase_difficulty', 'DIFFICULTY+'),
        ('ctrl+s', 'decrease_difficulty', 'DIFFICULTY-'),
        ('ctrl+z', 'restart', 'RESTART')
    ]

    CSS_PATH = DEFAULT_CSS_PATH

    textGenerator = TextGenerator(DEFAULT_TEXT_GENERATOR_SEED, DEFUALT_WORD_DICTIONARY_PATH, UNALLOWED_CHARS)

    difficulty = DEFAULT_DIFFICULTY
    wordCount = DEFUALT_WORD_COUNT
    maxWordLen = world_len_ranges[difficulty.value]


    # textToType = textGenerator.get_text(wordCount, maxWordLen)
    # textToType = "hello\nworld\nhi\nworld"
    textToType = "#include <stdio.h>\nmain(){\nprintf('Hello World');\nreturn 0;\n}"

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
        self.keyboardInput.border_subtitle = f"{repr(self.difficulty.name)} Difficulty"
        self.keyboardInput.styles.border_title_align = "center"
        self.keyboardInput.styles.border = ("heavy", "blue")

    def generate_new_text(self):
        self.textToType = self.textGenerator.get_text(self.wordCount, self.maxWordLen)

    def action_increase_words(self):
        self.wordCount+=1
        self.query_one('#keyboardInput').border_title = f"{self.wordCount} Word Test"
        self.generate_new_text()
        self.keyboardInput.update_text(self.textToType)

    def action_decrease_words(self):
        if(self.wordCount > 1):
            self.wordCount-=1
            self.query_one('#keyboardInput').border_title = f"{self.wordCount} Word Test"
            self.generate_new_text()
            self.keyboardInput.update_text(self.textToType)

    def get_range_from_difficulty(self):
        return world_len_ranges[self.difficulty.value]
    
    def update_maxWordLen(self):
        self.maxWordLen = self.get_range_from_difficulty()


    def action_increase_difficulty(self):
        new_difficulty_index = self.difficulty.value+1
        if(new_difficulty_index < len(order)):
            self.modify_difficulty(new_difficulty_index)

    def action_decrease_difficulty(self):
        new_difficulty_index = self.difficulty.value-1
        if(new_difficulty_index >= 0):
            self.modify_difficulty(new_difficulty_index)

    def modify_difficulty(self, new_difficulty_index):
        self.difficulty = order[new_difficulty_index]
        self.query_one('#keyboardInput').border_subtitle = f"{self.difficulty.name} Difficulty"
        self.update_maxWordLen()
        self.generate_new_text()
        self.keyboardInput.update_text(self.textToType)

    def action_restart(self):
        self.generate_new_text()
        self.keyboardInput.update_text(self.textToType)

    async def on_typing_completed(self, message: TypingCompleted):
        self.query_one('#wpmLabel').update(f"{message.wpm:.0f} WPM {message.cpm:.0f} CPM")
        self.attemptSidebar.add_entry(f"{message.wpm:.0f} WPM")



MyApp().run()