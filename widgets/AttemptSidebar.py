from textual import log
from textual.widget import Widget
from textual.widgets import Static, Collapsible

from messages.AttemptEntryClicked import AttemptEntryClicked

from screens.ResultsScreen import ResultsScreen

from widgets.AttemptEntry import AttemptEntry
from messages.TypingComplete import TypingCompleted


UNUSABLE_HEIGHT = 4
CSS_TOOLTIP_MAX_WIDTH = 60
POSTFIX_LENGTH = 3

class AttemptSidebar(Widget):

    def __init__(self,title: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.collapsibleGroup = Collapsible(id="attemptSidebarCollapsible", title=self.title, collapsed=False)
        self.entries = []
        self.attemptInfo = []
        self.entry_count = 0
        self.querry_counter = 0

    def compose(self):
        with self.collapsibleGroup:
            yield Static(f"", id='mainLabel')

    def on_mount(self):
        self.terminal_size = self.app.size

    def shorten_tooltip_length(self, tooltip):
        max_allowed_width = round(self.app.size.width*(CSS_TOOLTIP_MAX_WIDTH)/100)-POSTFIX_LENGTH
        if(len(tooltip[-1]) > max_allowed_width):
            tooltip[-1] = ''.join(list(tooltip[-1])[:max_allowed_width])+"...\""

        return tooltip

    async def on_attempt_entry_clicked(self, message: AttemptEntryClicked):
        self.app.push_screen(ResultsScreen(self.attemptInfo[message.position_index]))

    #TODO: Or make put it inside the scrollable container
    def add_entry(self, mainText: str, message: TypingCompleted):
        current_entry = AttemptEntry(f"[@click='noshit']{self.entry_count+1}. {mainText}[/]", id=f"entry_{self.entry_count}", classes="attemptEntry")
        
        tooltip = message.generate_tooltip()
        #Shorten the tooltip if needed
        tooltip = self.shorten_tooltip_length(tooltip)
        current_entry.tooltip = '\n'.join(tooltip)

        usable_terminal_height = self.terminal_size.height - UNUSABLE_HEIGHT
        
        if(usable_terminal_height < self.entry_count+1):
            valid_index = self.entry_count%usable_terminal_height
            current_entry.set_position_index(valid_index)

            self.entries[valid_index] = current_entry
            self.attemptInfo[valid_index] = message
            self.entry_count += 1

            self.collapsibleGroup.query_one(f'#entry_{self.querry_counter}').mount(current_entry)
            self.querry_counter += 1
        else:
            current_entry.set_position_index(self.entry_count)

            self.entries.append(current_entry)
            self.attemptInfo.append(message)
            self.entry_count += 1

            self.collapsibleGroup.query_one('#mainLabel').mount(current_entry)