from textual.widgets import Input
from rich.text import Text
from rich.style import Style
from textual.strip import Strip


class PersistentPlaceholderInput(Input):
    """An Input that keeps showing its placeholder while typing."""

    def render_line(self, y: int) -> Strip:
        logger = open('logs/PersistentPlaceholderTextArea_LOG.ini', 'w')
        if y != 0:
            return Strip.blank(self.size.width, self.rich_style)

        console = self.app.console
        console_options = self.app.console_options
        max_content_width = self.scrollable_content_region.width

        value_text = self._value
        text_length_before_ph = len(value_text)

        placeholder = ""
        if self.placeholder:
            typed_len = len(self.value)
            placeholder = self.placeholder[typed_len:]
            if placeholder:
                ph_text = Text(
                    placeholder,
                    style=self.get_component_rich_style("input--placeholder"),
                    no_wrap=True,
                    overflow="ignore",
                    end=""
                )
                value_text.append_text(ph_text)

        for i in range(len(self.placeholder)):
            logger.write(self.placeholder[i])
        logger.write('\n')
        
        HIGHLIGHT_STYLE = Style(bgcolor='red')

        for i in range(text_length_before_ph):
            if(self.placeholder[i] != value_text[i].plain):
                # if(value_text[i].plain == ' '):
                #     value_text = value_text[:i].append_text(Text('#')).append_text(value_text[i+1:])
                #     logger.write(f"After replacing: {value_text}")
                logger.write(f"Unmatch: {self.placeholder[i]} {value_text[i]} {i}\n")
                value_text.stylize(HIGHLIGHT_STYLE, i, i+1)


        if self.has_focus:
            if not self.selection.is_empty:
                start, end = sorted(self.selection)
                selection_style = self.get_component_rich_style("input--selection")
                value_text.stylize_before(selection_style, start, end)
            if self._cursor_visible:
                cursor_style = self.get_component_rich_style("input--cursor")
                cursor = self.cursor_position
                if self.cursor_at_end:
                    value_text.pad_right(1)
                value_text.stylize(cursor_style, cursor, cursor + 1)

        segments = list(
            console.render(value_text, console_options.update_width(max_content_width))
        )
        strip = Strip(segments)
        scroll_x, _ = self.scroll_offset
        strip = strip.crop(scroll_x, scroll_x + max_content_width + 1)
        strip = strip.extend_cell_length(max_content_width + 1)
        return strip.apply_style(self.rich_style)