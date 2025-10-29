from textual.app import App
from textual.widgets import Button, Label, Footer, Static, Collapsible, DataTable
from textual.widget import Widget
from textual.containers import Container
from textual import log

UNUSABLE_HEIGHT = 4

class AttemptSidebar(Widget):

    BINDINGS =[
        ('ctrl+f', 'add_entry', 'Add Entry'),
    ]

    def __init__(self,title: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.collapsibleGroup = Collapsible(id="attemptSidebarCollapsible", title=self.title)
        self.entries = []
        self.entry_count = 0


    def compose(self):
        with self.collapsibleGroup:
            yield Static(f"", id='mainLabel')


    def on_mount(self):
        self.terminal_size = self.app.size


    def action_add_entry(self):
        current_entry = Static(f"entry_{self.entry_count}", id=f"entry_{self.entry_count}")
        log(f"Terminal Height: {self.terminal_size.height}")
        usable_terminal_height = self.terminal_size.height - UNUSABLE_HEIGHT
        log(f"Usable Height: {usable_terminal_height}")
        log(f"entry_count: {self.entry_count}")

        if(usable_terminal_height < self.entry_count+1):
            valid_index = self.entry_count%usable_terminal_height
            log(f"entries: {self.entries}")
            log(f"valid_index: {valid_index}")
            self.entries[valid_index] = current_entry
            self.entry_count += 1
            self.collapsibleGroup.query_one(f'#entry_{valid_index}').mount(current_entry)
        else:
            self.entries.append(current_entry)
            self.entry_count += 1
            self.collapsibleGroup.query_one('#mainLabel').mount(current_entry)
