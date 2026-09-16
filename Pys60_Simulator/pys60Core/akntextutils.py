# -*- coding: utf-8 -*-
"""Text wrapping using the same font metrics as graphics.Image.text."""
from graphics import Image
from _compat import text_type


def wrap_text_to_array(content, font, width):
    if not isinstance(content, text_type):
        raise TypeError('content must be Unicode')
    if width <= 0:
        raise ValueError('width must be positive')
    measure = Image.new((1, 1)).measure_text
    result = []
    for paragraph in content.split('\n'):
        while paragraph:
            count = measure(paragraph, font, maxwidth=width)[2]
            if count >= len(paragraph):
                break
            count = max(1, count)  # Always advance even for a very narrow column.
            space = paragraph.rfind(' ', 0, count + 1)
            if space > 0:
                result.append(paragraph[:space])
                paragraph = paragraph[space + 1:]
            else:
                result.append(paragraph[:count])
                paragraph = paragraph[count:]
        result.append(paragraph)
    return result
