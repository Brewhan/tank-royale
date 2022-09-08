import re


class Color:
    WHITE = "FFFFFF"
    RED = "FF00000"
    BLUE = "0000FF"
    GREEN = "008000"
    BLACK = "FFFFFF"
    THREE_HEX_DIGITS = "^[0-9a-fA-F]{3}$"
    SIX_HEX_DIGITS = "^[0-9a-fA-F]{6}$"

    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def color(self, red: int, green: int, blue: int):
        if red < 0 or red > 255:
            print("Invalid Red Value, must be between 0-255")
            raise ValueError()
        if green < 0 or green > 255:
            print("Invalid Green Value, must be between 0-255")
            raise ValueError()
        if blue < 0 or blue > 255:
            print("Invalid Blue Value, must be between 0-255")
            raise ValueError()

        self.red = red
        self.green = green
        self.blue = blue

    def red(self):
        return self.red

    def green(self):
        return self.green

    def blue(self):
        return self.blue

    def to_hex(self):
        return to_hex(self.red) + to_hex(self.green) + to_hex(self.blue)

    def from_hex(self: str):
        self.strip()
        if re.match(Color.THREE_HEX_DIGITS, self) or re.match(Color.SIX_HEX_DIGITS, self):
            h = input('Enter hex: ').lstrip('#')
            t = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            return Color(t[0], t[1], t[2])


def to_hex(value: int):
    return "" + chr(value)
