#!/usr/bin/env python
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from asciiart import CHARS


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
        np.save("chars/chars.npy", [self.get_char_arr(char)
                                    for char in CHARS.values()])


if __name__ == '__main__':
    CharDictionary().get_char_dict()
