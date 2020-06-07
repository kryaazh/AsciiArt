#!/usr/bin/env python
import numpy as np
from PIL import Image, ImageFont, ImageDraw

chars = np.array([
    ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#',
    '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/',
    ':', ';', '?', '@', '\\', '^', '_', '`', '{', '|', '}',
    '~', '<', '=', '>'])


class CharDictionary:
    def __init__(self):
        self.char_dict = {}
        self.font = ImageFont.truetype("fonts/RobotoMono-Regular.ttf", 11)
        self.counter = 0

    def get_char_arr(self, char):
        char_width, char_height = self.font.getsize("|")
        char_img = Image.new('L', (char_width, char_height), 255)
        drawer = ImageDraw.Draw(char_img)
        drawer.text((0, 0), char, font=self.font, fill=0)
        return np.array(char_img)

    def get_char_dict(self):
        chars_arr = []
        for char in chars:
            chars_arr.append(self.get_char_arr(char))
        np.save("chars/chars.npy", chars_arr)


if __name__ == '__main__':
    CharDictionary().get_char_dict()
