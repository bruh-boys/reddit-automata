
from typing import Tuple

# this works for give a limit of words per line
# if you want to give a limit of characters per line
# you can use divide_text_width

def divide_text_width(text: str, width: int, text_size: int) -> list:
    output = []
    words = text.split(" ")

    text_line = ""
    if  len(text)*text_size<width-len(words[-1])*text_size:
        return words
    for word in words:
        if len(text_line)*text_size > width-len(word)*text_size:
            output.append(text_line)
            text_line = ""
        text_line += word+" "

    return output

# limit of lines per page

def divide_text_height(text: str, height: int, text_size: int) -> list:
    output = []
    lines = text.split("\n")

    text_lines = []
    if  len(lines)*text_size<height-text_size:
        return [text]
    for line in lines:
        if len(text_lines)*text_size > height-text_size:
            output.append("\n".join(text_lines))

            text_lines = []
        text_lines.append(line)

    return output

# this return you a list with the pages
# so you can make an animation or something with it
def divide_text(text: str, width: int, height: int, text_size: Tuple[int,int]) -> list:
    width_font_size, height_font_size = text_size
    lin = "\n".join(divide_text_width(text, width, width_font_size))

    pages = divide_text_height(lin, height, height_font_size)
 
    return pages

