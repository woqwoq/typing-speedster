from rich.segment import Segment
from rich.style import Style
from rich.console import Console
from textual.strip import Strip

console = Console()

segments = [Segment('asd', Style(bold=True)), Segment('red', Style(color='red'))]
segments2 = [Segment('blue', Style(color='blue')), Segment('purp', Style(color='purple'))]

strip1 = Strip(segments)
strip2 = Strip(segments2)

# Combine by concatenating their segments
combined = Strip(list(strip1) + list(strip2))
newElement = combined[4].apply_style(Style(bgcolor='white'))
print(combined[:4])
# combined = combined[:4] + newElement + combined[5:]
