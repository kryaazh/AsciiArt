#!/usr/bin/env python

import numpy as np
from PIL import Image, ImageFont, ImageDraw
import os

chars = np.array([' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                  'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                  'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                  'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                  'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#',
                  '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/',
                  ':', ';', '?', '@', '\\', '^', '_', '`', '{', '|', '}',
                  '~', '<', '=', '>'
                  ])


class CharDictionary:
    def __init__(self):
        self.char_dict = {}
        self.font = ImageFont.truetype("fonts\\RobotoMono-Regular.ttf", 14)
        self.counter = 0

    def get_char_img(self, char):
        char_width, char_height = self.font.getsize("|")
        char_img = Image.new('L', (char_width, char_height), 255)
        drawer = ImageDraw.Draw(char_img)
        drawer.text((0, 0), char, font=self.font, fill=0)

        char_img.save(f'''chars\\{self.counter}.jpg''')
        return char_img

    def get_char_dict(self):
        files = os.listdir("chars")

        if not files:
            self.counter = 0
            for char in chars:
                char_img = self.get_char_img(char)
                self.char_dict[char] = char_img
                self.counter += 1
        else:
            self.counter = 0
            for char in chars:
                char_img = Image.open(f'''chars\\{self.counter}.jpg''')
                self.char_dict[char] = char_img
                self.counter += 1


if __name__ == '__main__':
    CharDictionary().get_char_dict()
