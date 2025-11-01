from rich.segment import Segment
from rich.style import Style
from rich.console import Console
from textual.strip import Strip
from rich.text import Text

from TextGenerator import TextGenerator

console = Console()

asd = TextGenerator(123, "The_Oxford_3000.txt", {})

t1 = Text(asd.get_text(5, 3))

console.print(t1)
