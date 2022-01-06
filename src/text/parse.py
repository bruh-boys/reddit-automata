
#sex
#sex
def divide_text_width(text: str, width: int, text_size: int) -> list:
    output = []
    words = text.split(" ")

    text_line = ""

    for word in words:
        if len(text_line)*text_size > width-len(word)*text_size:
            output.append(text_line)
            text_line = ""
        text_line += word+" "

    return output


def divide_text_height(text: str, height: int, text_size: int) -> list:
    output = []
    lines = text.split("\n")

    text_lines = []

    for line in lines:
        if len(text_lines)*text_size > height-text_size:
            output.append("\n".join(text_lines))

            text_lines = []
        text_lines.append(line)

    return output


def divide_text(text: str, width: int, height: int, text_size: int) -> list:
    lin = "\n".join(divide_text_width(text, width, text_size))

    pages = divide_text_height(lin, height, text_size)
    return pages


f = open("test.txt", "r")
text = f.read()

lin = "\n".join(divide_text_width(text, 720, 10))
pages = divide_text_height(lin, 720, 10)

print("\n\n".join(pages))
