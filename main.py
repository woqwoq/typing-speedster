from textual.app import App, SystemCommand
from textual.widgets import Label, Footer
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen

from core.Difficulty import Difficulty, world_len_ranges, difficulty_order
from core.Mode import Mode, mode_order
from core.TextGenerator import TextGenerator

from widgets.AttemptSidebar import AttemptSidebar
from widgets.KeypressDisplay import KeypressDisplay
from widgets.StaticKeyboardInput import StaticKeyboardInput
from widgets.StaticKeyboardInputSpec import StaticKeyboardInputSpec

from screens.ResultsScreen import ResultsScreen

from messages.TypingComplete import TypingCompleted


# ============================================================
# CONSTANTS & CONFIG
# ============================================================
UNALLOWED_CHARS = {",", ".", "'", "-"}

DEFAULT_MODE = Mode.TEXT
DEFAULT_DIFFICULTY = Difficulty.EASY
DEFAULT_WORD_COUNT = 5
DEFAULT_MAX_WORD_LENGTH = world_len_ranges[DEFAULT_DIFFICULTY.value]

DEFAULT_CSS_PATH = "styles/App.css"
DEFAULT_SEED = 123

DEFAULT_DICT_WORDS = "dicts/The_Oxford_3000.txt"
DEFAULT_DICT_LYRICS = "dicts/Lyrics.txt"
DEFAULT_DICT_QUOTES = "dicts/Quotes.txt"
DEFAULT_DICT_CODE = "dicts/Code.txt"


# ============================================================
# APPLICATION
# ============================================================
class MyApp(App):

    CSS_PATH = DEFAULT_CSS_PATH

    BINDINGS = [
        ("ctrl+d", "increase_words", "WORDS+"),
        ("ctrl+a", "decrease_words", "WORDS-"),
        ("ctrl+w", "increase_difficulty", "DIFFICULTY+"),
        ("ctrl+s", "decrease_difficulty", "DIFFICULTY-"),
        ("ctrl+z", "restart", "RESTART"),
        ("ctrl+r", "next_mode", "MODE"),
        ("ctrl+x", "reset_text", "RESET"),
    ]

    # --------------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------------
    mode = DEFAULT_MODE
    difficulty = DEFAULT_DIFFICULTY
    wordCount = DEFAULT_WORD_COUNT
    maxWordLen = DEFAULT_MAX_WORD_LENGTH

    textGenerator = TextGenerator(
        DEFAULT_SEED,
        DEFAULT_DICT_WORDS,
        DEFAULT_DICT_LYRICS,
        DEFAULT_DICT_QUOTES,
        DEFAULT_DICT_CODE,
        UNALLOWED_CHARS,
    )

    textToType = textGenerator.get_text(mode, wordCount, maxWordLen)

    # --------------------------------------------------------
    # UI COMPONENTS
    # --------------------------------------------------------
    welcomeLabel = Label(id="welcomeLabel", content="Typing-Speedster")

    keyboardInput = StaticKeyboardInputSpec(id="keyboardInput", placeholder=textToType)
    keyboardInputContainer = ScrollableContainer(keyboardInput, id="keyboardInputContainer")

    labels = Container(
        Label("15", id="timerLabel"),
        Label("", id="wpmLabel"),
        id="labelContainer",
    )

    attemptSidebar = AttemptSidebar(id="attemptSidebarCollapsible", title="Previous Attempts")

    resultsScreen = None

    # ============================================================
    # COMPOSITION
    # ============================================================
    def compose(self):
        yield self.welcomeLabel
        yield self.labels
        yield self.keyboardInputContainer
        yield self.attemptSidebar
        # yield self.keypressDisplayContainer
        yield Footer()

    def on_mount(self):
        self.update_labels()
        self.keyboardInputContainer.styles.border_title_align = "center"
        self.keyboardInputContainer.styles.border = ("heavy", "blue")

    # ============================================================
    # HELPERS
    # ============================================================
    def refresh_text_and_ui(self):
        self.textToType = self.textGenerator.get_text(self.mode, self.wordCount, self.maxWordLen)
        self.update_labels()
        self.keyboardInput.update_text(self.textToType)

    def update_labels(self):
        container = self.query_one("#keyboardInputContainer")
        container.border_title = self._generate_label()
        container.border_subtitle = f"{self.mode.name} | {self.difficulty.name}"

    def _generate_label(self):
        if self.mode is Mode.TEXT:
            return f"{self.wordCount} Word Test"
        return self.textGenerator.recent_description

    # ============================================================
    # SYSTEM COMMANDS
    # ============================================================
    def get_system_commands(self, screen: Screen):
        yield from super().get_system_commands(screen)
        yield SystemCommand("Restart Test", "Restart the test with a new text", self.action_restart)
        yield SystemCommand("Reset Test", "Reset the test keeping same text", self.action_reset_text)
        yield SystemCommand("Switch Mode", f"Mode order: {[m.name for m in mode_order]}", self.action_next_mode)
        yield SystemCommand("Increase Word Count", "", self.action_increase_words)
        yield SystemCommand("Decrease Word Count", "", self.action_decrease_words)
        yield SystemCommand("Increase Difficulty", "", self.action_increase_difficulty)
        yield SystemCommand("Decrease Difficulty", "", self.action_decrease_difficulty)

    # ============================================================
    # ACTIONS
    # ============================================================
    def action_increase_words(self):
        self.wordCount += 1
        self.refresh_text_and_ui()

    def action_decrease_words(self):
        if self.wordCount > 1:
            self.wordCount -= 1
            self.refresh_text_and_ui()

    def action_increase_difficulty(self):
        new_index = self.difficulty.value + 1
        if new_index < len(difficulty_order):
            self.difficulty = difficulty_order[new_index]
            self.maxWordLen = world_len_ranges[new_index]
            self.refresh_text_and_ui()

    def action_decrease_difficulty(self):
        new_index = self.difficulty.value - 1
        if new_index >= 0:
            self.difficulty = difficulty_order[new_index]
            self.maxWordLen = world_len_ranges[new_index]
            self.refresh_text_and_ui()

    def action_restart(self):
        self.refresh_text_and_ui()

    def action_next_mode(self):
        new_index = (self.mode.value + 1) % len(mode_order)
        self.mode = mode_order[new_index]
        self.refresh_text_and_ui()

    def action_reset_text(self):
        self.keyboardInput.reset_text()

    # ============================================================
    # MESSAGE LISTENERS
    # ============================================================
    async def on_typing_completed(self, message: TypingCompleted):
        self.query_one("#wpmLabel").update(f"{message.wpm:.0f} WPM {message.cpm:.0f} CPM")
        message.difficulty = self.difficulty
        self.attemptSidebar.add_entry(f"{message.wpm:.0f} WPM", message)

        self.resultsScreen = ResultsScreen(message)
        self.push_screen(self.resultsScreen)

    # async def on_key_pressed(self, message: KeyPressed):
    #     key = message.key.lower()
    #     self.keypressDisplay.highlight_key(key)
    #ASYNC MESSAGE LISTENERS

MyApp().run()