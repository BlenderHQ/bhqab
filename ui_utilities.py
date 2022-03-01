"""The module also has functionality for formatting a block of text when
displaying it in the Blender user interface.
"""

import bpy
import blf

WIN_PADDING = 32


def _string_width(string: str) -> float:
    if len(string) == 1:
        num_single_ch_samples = 100
        return blf.dimensions(0, string * num_single_ch_samples)[0] / num_single_ch_samples
    return blf.dimensions(0, string)[0]


def draw_wrapped_text(context: bpy.types.Context, layout: bpy.types.UILayout, text: str) -> None:
    """Draws a block of text in the given layout, dividing it into lines
    according to the width of the current region of the interface.

    .. Warning::
        The function uses a fairly accurate but at the same time relatively slow
        way to format strings. Not recommended for use with very large blocks
        of text as this may slow down the overall user interface.

    Args:
        context (bpy.types.Context): Current context.
        layout (bpy.types.UILayout): Current layout.
        text (str): Text to be wrapped and drawn.
    """

    col = layout.column(align=True)

    wrap_width = context.region.width - WIN_PADDING
    space_width = _string_width(' ')

    for line in text.split('\n'):
        num_characters = len(line)

        if not num_characters:
            continue

        line_words = list((_, _string_width(_)) for _ in line.split(' '))
        num_line_words = len(line_words)
        line_words_last = num_line_words - 1

        sublines = [""]
        subline_width = 0.0

        for i in range(num_line_words):
            word, word_width = line_words[i]

            sublines[-1] += word
            subline_width += word_width

            next_word_width = 0.0
            if i < line_words_last:
                next_word_width = line_words[i + 1][1]

                sublines[-1] += ' '
                subline_width += space_width

            if subline_width + next_word_width > wrap_width:
                subline_width = 0.0
                if i < line_words_last:
                    sublines.append("")  # Add new subline.

        for subline in sublines:
            col.label(text=subline)
