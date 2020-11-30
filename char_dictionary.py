#!/usr/bin/env python
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from ascii_art import CHARS
import argparse


def parse():
    parser = argparse.ArgumentParser(add_help=True,
                                     description="Image to ASCII")
    parser.add_argument('-f', '--font', dest='font',
                        default="font/RobotoMono-Regular.ttf",
                        help="Font which will be used")
    parser.add_argument('-s', '--chars_file', dest='chars',
                        default="chars/chars.npy",
                        help="File .npy in which to save the dictionary")
    return parser.parse_args()


class CharDictionary:
    def __init__(self, font, chars):
        self.font = font
        self.chars = chars
        self.char_dict = {}
        self.font = ImageFont.truetype(self.font, 11)

    def get_char_arr(self, char):
        char_width, char_height = self.font.getsize("|")
        char_img = Image.new('L', (char_width, char_height), 255)
        drawer = ImageDraw.Draw(char_img)
        drawer.text((0, 0), char, font=self.font, fill=0)
        return np.array(char_img)

    def get_char_dict(self):
        np.save(self.chars, [self.get_char_arr(char)
                             for char in CHARS.values()])


if __name__ == '__main__':
    args = parse()
    CharDictionary(args.font, args.chars).get_char_dict()
