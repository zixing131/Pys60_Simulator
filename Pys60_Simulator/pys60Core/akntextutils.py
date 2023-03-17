# -*- coding: utf-8 -*-
import tkFont


def wrap_text_to_array(content, dense, width):
    font = tkFont.Font(family=dense, size=15)
    result = []
    temp_str = ''

    for char in content:
        if char == '\n':
            result.append(temp_str)
            temp_str = ''
            continue
        temp_str += char
        char_width = font.measure(temp_str)

        if char_width >= width:
            result.append(temp_str)
            temp_str = ''

    if temp_str:
        result.append(temp_str)

    return result
