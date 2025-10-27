from textual.strip import Strip
from textual.widgets import TextArea

from rich.style import Style
from rich.segment import Segment
from rich.text import Text

class PersistentPlaceholderTextArea(TextArea):
    def _render_line(self, y: int) -> Strip:
        logger = open('render_line_log.ini', 'w')
        """Render a single line of the PersistentPlaceholderTextArea. Called by Textual.

        Args:
            y: Y Coordinate of line relative to the widget region.

        Returns:
            A rendered line.
        """
        theme = self._theme
        base_style = (
            theme.base_style
            if theme and theme.base_style is not None
            else self.rich_style
        )

        wrapped_document = self.wrapped_document
        scroll_x, scroll_y = self.scroll_offset

        # Account for how much the PersistentPlaceholderTextArea is scrolled.
        y_offset = y + scroll_y

        # If we're beyond the height of the document, render blank lines
        out_of_bounds = y_offset >= wrapped_document.height

        if out_of_bounds:
            return Strip.blank(self.size.width, base_style)

        # Get the line corresponding to this offset
        try:
            line_info = wrapped_document._offset_to_line_info[y_offset]
        except IndexError:
            line_info = None

        if line_info is None:
            return Strip.blank(self.size.width, base_style)

        line_index, section_offset = line_info

        line = self.get_line(line_index)
        line_character_count = len(line)
        line.tab_size = self.indent_width
        line.set_length(line_character_count)  # space at end for cursor
        virtual_width, _virtual_height = self.virtual_size

        selection = self.selection
        start, end = selection
        cursor_row, cursor_column = end

        selection_top, selection_bottom = sorted(selection)
        selection_top_row, selection_top_column = selection_top
        selection_bottom_row, selection_bottom_column = selection_bottom

        highlight_cursor_line = self.highlight_cursor_line and self._has_cursor
        cursor_line_style = (
            theme.cursor_line_style if (theme and highlight_cursor_line) else None
        )
        has_cursor = self._has_cursor

        if has_cursor and cursor_line_style and cursor_row == line_index:
            line.stylize(cursor_line_style)

        # Selection styling
        if start != end and selection_top_row <= line_index <= selection_bottom_row:
            # If this row intersects with the selection range
            selection_style = theme.selection_style if theme else None
            cursor_row, _ = end
            if selection_style:
                if line_character_count == 0 and line_index != cursor_row:
                    # A simple highlight to show empty lines are included in the selection
                    line.plain = "▌"
                    line.stylize(Style(color=selection_style.bgcolor))
                else:
                    if line_index == selection_top_row == selection_bottom_row:
                        # Selection within a single line
                        line.stylize(
                            selection_style,
                            start=selection_top_column,
                            end=selection_bottom_column,
                        )
                    else:
                        # Selection spanning multiple lines
                        if line_index == selection_top_row:
                            line.stylize(
                                selection_style,
                                start=selection_top_column,
                                end=line_character_count,
                            )
                        elif line_index == selection_bottom_row:
                            line.stylize(selection_style, end=selection_bottom_column)
                        else:
                            line.stylize(selection_style, end=line_character_count)

        highlights = self._highlights
        if highlights and theme:
            line_bytes = _utf8_encode(line.plain)
            byte_to_codepoint = build_byte_to_codepoint_dict(line_bytes)
            get_highlight_from_theme = theme.syntax_styles.get
            line_highlights = highlights[line_index]
            for highlight_start, highlight_end, highlight_name in line_highlights:
                node_style = get_highlight_from_theme(highlight_name)
                if node_style is not None:
                    line.stylize(
                        node_style,
                        byte_to_codepoint.get(highlight_start, 0),
                        byte_to_codepoint.get(highlight_end) if highlight_end else None,
                    )

        HIGHLIGHT_STYLE = Style(bgcolor='red')
            
        line_len = len(line)
        ph_line = Text(self.placeholder[line_len:], Style(dim=True))
        line += ph_line

        for i in range(line_len):
            if line[i].plain != self.placeholder[i]:
                line.stylize(HIGHLIGHT_STYLE, i, i+1)

        # Highlight the cursor
        matching_bracket = self._matching_bracket_location
        match_cursor_bracket = self.match_cursor_bracket
        draw_matched_brackets = (
            has_cursor
            and match_cursor_bracket
            and matching_bracket is not None
            and start == end
        )

        if cursor_row == line_index:
            draw_cursor = self._draw_cursor
            if draw_matched_brackets:
                matching_bracket_style = theme.bracket_matching_style if theme else None
                if matching_bracket_style:
                    line.stylize(
                        matching_bracket_style,
                        cursor_column,
                        cursor_column + 1,
                    )

            if self.suggestion and (self.has_focus or not self.hide_suggestion_on_blur):
                suggestion_style = self.get_component_rich_style(
                    "text-area--suggestion"
                )
                line = Text.assemble(
                    line[:cursor_column],
                    (self.suggestion, suggestion_style),
                    line[cursor_column:],
                )

            if draw_cursor:
                cursor_style = theme.cursor_style if theme else None
                if cursor_style:
                    line.stylize(cursor_style, cursor_column, cursor_column + 1)

        # Highlight the partner opening/closing bracket.
        if draw_matched_brackets:
            # mypy doesn't know matching bracket is guaranteed to be non-None
            assert matching_bracket is not None
            bracket_match_row, bracket_match_column = matching_bracket
            if theme and bracket_match_row == line_index:
                matching_bracket_style = theme.bracket_matching_style
                if matching_bracket_style:
                    line.stylize(
                        matching_bracket_style,
                        bracket_match_column,
                        bracket_match_column + 1,
                    )

        # Build the gutter text for this line
        gutter_width = self.gutter_width
        if self.show_line_numbers:
            if cursor_row == line_index and highlight_cursor_line:
                gutter_style = theme.cursor_line_gutter_style
            else:
                gutter_style = theme.gutter_style

            gutter_width_no_margin = gutter_width - 2
            gutter_content = (
                str(line_index + self.line_number_start) if section_offset == 0 else ""
            )
            gutter = [
                Segment(f"{gutter_content:>{gutter_width_no_margin}}  ", gutter_style)
            ]
        else:
            gutter = []

        # TODO: Lets not apply the division each time through render_line.
        #  We should cache sections with the edit counts.
        wrap_offsets = wrapped_document.get_offsets(line_index)
        if wrap_offsets:
            sections = line.divide(wrap_offsets)  # TODO cache result with edit count
            line = sections[section_offset]
            line_tab_widths = wrapped_document.get_tab_widths(line_index)
            line.end = ""

            # Get the widths of the tabs corresponding only to the section of the
            # line that is currently being rendered. We don't care about tabs in
            # other sections of the same line.

            # Count the tabs before this section.
            tabs_before = 0
            for section_index in range(section_offset):
                tabs_before += sections[section_index].plain.count("\t")

            # Count the tabs in this section.
            tabs_within = line.plain.count("\t")
            section_tab_widths = line_tab_widths[
                tabs_before : tabs_before + tabs_within
            ]
            line = expand_text_tabs_from_widths(line, section_tab_widths)
        else:
            line.expand_tabs(self.indent_width)

        base_width = (
            self.scrollable_content_region.size.width
            if self.soft_wrap
            else max(virtual_width, self.region.size.width)
        )
        target_width = base_width - self.gutter_width


        #START
        

        # Crop the line to show only the visible part (some may be scrolled out of view)
        console = self.app.console
        text_strip = Strip(line.render(console), cell_length=line.cell_len)

        if not self.soft_wrap:
            text_strip = text_strip.crop(scroll_x, scroll_x + virtual_width)

        # Stylize the line the cursor is currently on.
        if cursor_row == line_index and self.highlight_cursor_line:
            line_style = cursor_line_style
        else:
            line_style = theme.base_style if theme else None

        text_strip = text_strip.extend_cell_length(target_width, line_style)
        if gutter:
            strip = Strip.join([Strip(gutter, cell_length=gutter_width), text_strip])
        else:
            strip = text_strip

        logger.write("\nFinal Strip: " + str(strip))

        return strip.apply_style(base_style)
