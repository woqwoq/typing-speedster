from textual import log

from textual.app import App
from textual.widgets import Label, Footer
from textual.containers import Container, ScrollableContainer

from widgets.AttemptSidebar import AttemptSidebar
from widgets.KeypressDisplay import KeypressDisplay
from widgets.StaticKeyboardInput import StaticKeyboardInput

from screens.ResultsScreen import ResultsScreen

from messages.TypingComplete import TypingCompleted
from messages.KeyPressed import KeyPressed

from core.Difficulty import Difficulty, world_len_ranges, difficulty_order
from core.TextGenerator import TextGenerator
from core.Mode import Mode, mode_order


UNALLOWED_CHARS = {',', '.', "'", "-"}

DEFAULT_MODE = Mode.TEXT
DEFAULT_DIFFICULTY = Difficulty.EASY
DEFUALT_WORD_COUNT = 5
DEFAULT_CSS_PATH = "styles/App.css"
DEFAULT_TEXT_GENERATOR_SEED = 123
DEFUALT_WORD_DICTIONARY_PATH = "dicts/The_Oxford_3000.txt"
DEFAULT_LYRICS_DICTIONARY_PATH = "dicts/Lyrics.txt"
DEFAULT_QUOTE_DICTIONARY_PATH = "dicts/Quotes.txt"
DEFAULT_CODE_DICTIONARY_PATH = "dicts/Code.txt"

class MyApp(App):

    BINDINGS =[
        ('ctrl+d', 'increase_words', 'WORDS+'),
        ('ctrl+a', 'decrease_words', 'WORDS-'),
        ('ctrl+w', 'increase_difficulty', 'DIFFICULTY+'),
        ('ctrl+s', 'decrease_difficulty', 'DIFFICULTY-'),
        ('ctrl+z', 'restart', 'RESTART'),
        ('ctrl+r', 'next_mode', 'MODE')
    ]

    CSS_PATH = DEFAULT_CSS_PATH

    mode = DEFAULT_MODE

    textGenerator = TextGenerator(DEFAULT_TEXT_GENERATOR_SEED, DEFUALT_WORD_DICTIONARY_PATH,
                                   DEFAULT_LYRICS_DICTIONARY_PATH, DEFAULT_QUOTE_DICTIONARY_PATH, 
                                   DEFAULT_CODE_DICTIONARY_PATH, UNALLOWED_CHARS)

    difficulty = DEFAULT_DIFFICULTY
    wordCount = DEFUALT_WORD_COUNT
    maxWordLen = world_len_ranges[difficulty.value]


    textToType = textGenerator.get_text(mode, wordCount, maxWordLen)
    # textToType = "hello\nworld\nhi\nworld\na\ns\nhi\nworld\na\ns"
    # textToType = """class TabExampleApp(App):\n\tdef compose(self) -> ComposeResult:\n\t\tyield TextArea(id="editor")\n\t\tyield Input(placeholder="Type here...")"""

    welcomeLabel = Label(id='welcomeLabel', content="Typing-Speedster")

    keyboardInput = StaticKeyboardInput(id='keyboardInput', placeholder=textToType)
    keyboardInputContainer = ScrollableContainer(keyboardInput, id="keyboardInputContainer")

    labels = Container( Label("15", id="timerLabel"), Label("", id="wpmLabel"), id="labelContainer")

    attemptSidebar = AttemptSidebar(id='attemptSidebarCollapsible', title='Previous Attempts')

    keypressDisplay = KeypressDisplay(id="keypressDisplay")

    keypressDisplayContainer = Container(keypressDisplay, id="keypressDisplayContainer")

    resultsScreen = None

    def compose(self):
        yield self.welcomeLabel
        yield self.labels
        yield self.keyboardInputContainer
        yield self.attemptSidebar
        yield self.keypressDisplayContainer
        yield Footer()

    def on_mount(self):
        self.keyboardInputContainer.border_title = f"{self.wordCount} Word Test"
        self.keyboardInputContainer.border_subtitle = f"{self.mode.name} | {self.difficulty.name}"
        self.keyboardInputContainer.styles.border_title_align = "center"
        self.keyboardInputContainer.styles.border = ("heavy", "blue")

    def generate_new_text(self):
        self.textToType = self.textGenerator.get_text(self.mode, self.wordCount, self.maxWordLen)

    def action_increase_words(self):
        self.wordCount+=1
        self.query_one('#keyboardInputContainer').border_title = f"{self.wordCount} Word Test"
        self.generate_new_text()
        self.keyboardInput.update_text(self.textToType, self.difficulty)

    def action_decrease_words(self):
        if(self.wordCount > 1):
            self.wordCount-=1
            self.query_one('#keyboardInputContainer').border_title = f"{self.wordCount} Word Test"
            self.generate_new_text()
            self.keyboardInput.update_text(self.textToType, self.difficulty)

    def get_range_from_difficulty(self):
        return world_len_ranges[self.difficulty.value]
    
    def update_maxWordLen(self):
        self.maxWordLen = self.get_range_from_difficulty()

    def action_increase_difficulty(self):
        new_difficulty_index = self.difficulty.value+1
        if(new_difficulty_index < len(difficulty_order)):
            self.modify_difficulty(new_difficulty_index)

    def action_decrease_difficulty(self):
        new_difficulty_index = self.difficulty.value-1
        if(new_difficulty_index >= 0):
            self.modify_difficulty(new_difficulty_index)

    def modify_difficulty(self, new_difficulty_index):
        self.difficulty = difficulty_order[new_difficulty_index]
        self.query_one('#keyboardInputContainer').border_subtitle = f"{self.mode.name} | {self.difficulty.name}"
        self.update_maxWordLen()
        self.generate_new_text()
        self.keyboardInput.update_text(self.textToType, self.difficulty)

    def action_restart(self):
        self.generate_new_text()
        self.keyboardInput.update_text(self.textToType, self.difficulty)

    def activate_screen(self, message: TypingCompleted):
        self.resultsScreen = ResultsScreen(message)
        self.push_screen(self.resultsScreen)

    def action_attempt_clicked(self):
        log("clicked")

    def change_mode(self):
        self.query_one('#keyboardInputContainer').border_subtitle = f"{self.mode.name} | {self.difficulty.name}"

        self.generate_new_text()
        self.keyboardInput.update_text(self.textToType, self.difficulty)

    def action_next_mode(self):
        new_mode_index = (self.mode.value+1)%len(mode_order)
        self.mode = mode_order[new_mode_index]
        
        self.change_mode()

    async def on_typing_completed(self, message: TypingCompleted):
        self.query_one('#wpmLabel').update(f"{message.wpm:.0f} WPM {message.cpm:.0f} CPM")
        self.attemptSidebar.add_entry(f"{message.wpm:.0f} WPM", message)

        self.activate_screen(message)

    async def on_key_pressed(self, message: KeyPressed):
        key = message.key.lower()
        self.keypressDisplay.highlight_key(key)

MyApp().run()