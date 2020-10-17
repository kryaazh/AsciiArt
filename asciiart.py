#!/usr/bin/env python
import cv2
import sys
import os
import numpy as np
from PIL import ImageChops, Image
import ParserArguments as parser

CHARS = {
    0:  ' ', 1:  '0', 2:  '1', 3:  '2', 4:  '3', 5:  '4', 6: '5',
    7:  '6', 8:  '7', 9:  '8', 10: '9', 11: 'a', 12: 'b',
    13: 'c', 14: 'd', 15: 'e', 16: 'f', 17: 'g', 18: 'h',
    19: 'i', 20: 'j', 21: 'k', 22: 'l', 23: 'm', 24: 'n',
    25: 'o', 26: 'p', 27: 'q', 28: 'r', 29: 's', 30: 't',
    31: 'u', 32: 'v', 33: 'w', 34: 'x', 35: 'y', 36: 'z',
    37: 'A', 38: 'B', 39: 'C', 40: 'D', 41: 'E', 42: 'F',
    43: 'G', 44: 'H', 45: 'I', 46: 'J', 47: 'K', 48: 'L',
    49: 'M', 50: 'N', 51: 'O', 52: 'P', 53: 'Q', 54: 'R',
    55: 'S', 56: 'T', 57: 'U', 58: 'V', 59: 'W', 60: 'X',
    61: 'Y', 62: 'Z', 63: '!', 64: '"', 65: '#', 66: '$',
    67: '%', 68: '&', 69: '(', 70: ')', 71: '*', 72: '+',
    73: ',', 74: '-', 75: '.', 76: '/', 77: ':', 78: ';',
    79: '?', 80: '@', 81: '\\', 82: '^', 83: '_', 84: '`',
    85: '{', 86: '|', 87: '}', 88: '~', 89: '<', 90: '=', 91: '>'}
CHAR_DICT = np.load("chars/chars.npy")
BLOCK_WIDTH = 7
BLOCK_HEIGHT = 14


class ImageConverter:
    def __init__(self, width, height, invert, contrast):
        self.width = width
        self.height = height
        self.invert = invert
        self.contrast = contrast

    @staticmethod
    def resize(img, width, height):
        _new_width = 0
        _new_height = 0
        _width, _height = img.size
        ratio = _height / _width

        if width and height:
            _new_width = width
            _new_height = height
        elif not width and not height:
            _new_width = 120
            _new_height = ratio * _new_width
        elif width and not height:
            _new_width = width
            _new_height = ratio * _new_width
        elif height and not width:
            _new_height = height
            _new_width = height / ratio

        return img.resize((int(_new_width), int(_new_height)))

    @staticmethod
    def get_size_in_blocks(img):
        return int(img.size[0] / BLOCK_WIDTH), int(img.size[1] / BLOCK_HEIGHT)

    @staticmethod
    def change_contrast(img, level):
        factor = (259 * (level + 255)) / (255 * (259 - level))

        def contrast(c):
            value = 128 + factor * (c - 128)
            return max(0, min(255, value))
        return img.point(contrast)

    @staticmethod
    def to_gray_scale(img):
        img_arr = np.array(img)
        gs_factors = np.array([0.2989, 0.587, 0.114])
        width, height = img_arr.shape[0], img_arr.shape[1]
        try:
            img_arr.reshape(width * height, 3)
            out = np.matmul(img_arr, gs_factors)
        except ValueError:
            return img_arr
        return out.reshape(width, height)

    def to_ascii_chars(self, img):
        count_block_w, count_block_h = self.get_size_in_blocks(img)
        new_pixels = []
        for y in range(count_block_h):
            for x in range(count_block_w):
                new_pixels.append(self.get_most_suitable_char(img, x, y))
        new_pixels = ''.join(new_pixels)

        ascii_img = [new_pixels[i:i + count_block_w]
                     for i in range(0, len(new_pixels), count_block_w)]
        ascii_img = "\n".join(ascii_img)

        return ascii_img

    def get_most_suitable_char(self, img, x, y):
        min_diff = sys.maxsize
        most_suitable_char = " "
        next_x = x * BLOCK_WIDTH
        next_y = y * BLOCK_HEIGHT
        block = np.array(img.crop(
            (next_x, next_y, next_x + BLOCK_WIDTH, next_y + BLOCK_HEIGHT)))

        for i in range(92):
            if self.invert:
                difference = np.sum(abs((254 - CHAR_DICT[i, :]) - block))
            else:
                difference = np.sum(abs(CHAR_DICT[i, :] - block))
            if difference < min_diff:
                min_diff = difference
                most_suitable_char = CHARS[i]
        return most_suitable_char

    def convert(self, img):
        resize_img = self.resize(img,
                                 self.width * BLOCK_WIDTH,
                                 self.height * BLOCK_HEIGHT)
        contrast_img = self.change_contrast(resize_img, self.contrast)
        gs_img = contrast_img.convert('L')
        if self.invert:
            gs_img = ImageChops.invert(gs_img)
        out_ascii = self.to_ascii_chars(gs_img)

        return out_ascii


def get_result_image():
    _parser = parser.ParserArguments()
    img_file, out_file, width, height, invert, contrast = _parser.parse()
    converter = ImageConverter(width, height, invert, contrast)
    ascii_image = converter.convert(Image.open(img_file))

    if out_file is None:
        sys.stdout.write(ascii_image)
    else:
        with open(out_file, 'w') as file:
            file.write(ascii_image)


def main():
    get_result_image()


if __name__ == '__main__':
    main()
