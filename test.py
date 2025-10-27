from rich.segment import Segment
from rich.style import Style
from rich.console import Console
from textual.strip import Strip
from rich.text import Text

console = Console()

t1 = Text("asd")
t2 = Text("fas")

console.print(t1)
console.print(t2)
console.print(t1+t2)