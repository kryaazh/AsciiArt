#!/usr/bin/env python
import sys
import numpy as np
from PIL import Image, ImageChops
import ParserArguments as parse

chars = {
    0: ' ', 1: '0', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5',
       7: '6', 8: '7', 9: '8', 10: '9', 11: 'a', 12: 'b',
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
block_width = 7
block_height = 14


class ImageConverter:
    def __init__(self, img_file, out_file,
                 arg_width, arg_height, arg_invert, arg_contrast):
        self.img = Image.open(img_file)
        self.out_file = out_file
        self.width, self.height = self.img.size
        self.arg_width = arg_width
        self.arg_height = arg_height
        self.invert = arg_invert
        self.contrast = arg_contrast

    def resize(self, img, arg_width, arg_height):
        new_width = 0
        new_height = 0
        ratio = self.height / self.width

        if arg_width is not None and arg_height is not None:
            new_width = arg_width
            new_height = arg_height

        elif arg_width is None and arg_height is None:
            new_width = 1200
            new_height = ratio * new_width

        elif arg_width is not None and arg_height is None:
            new_width = arg_width
            new_height = ratio * new_width

        elif arg_height is not None and arg_width is None:
            new_height = arg_height
            new_width = arg_height / ratio

        return img.resize((int(new_width), int(new_height)))

    @staticmethod
    def get_size_in_blocks(img):
        count_block_w = int(img.size[0] / block_width)
        count_block_h = int(img.size[1] / block_height)

        return count_block_w, count_block_h

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
        char_dict = np.load("chars/chars.npy")

        min_diff = sys.maxsize
        most_suitable_char = " "
        next_x = x * block_width
        next_y = y * block_height
        block = np.array(img.crop(
            (next_x, next_y, next_x + block_width, next_y + block_height)))

        for i in range(92):
            if self.invert:
                difference = np.sum(abs((254 - char_dict[i, :]) - block))
            else:
                difference = np.sum(abs(char_dict[i, :] - block))
            if difference < min_diff:
                min_diff = difference
                most_suitable_char = chars[i]
        return most_suitable_char

    def convert(self):
        resize_img = self.resize(self.img, self.arg_width, self.arg_height)
        contrast_img = self.change_contrast(resize_img, self.contrast)
        gs_img = contrast_img.convert('L')

        if self.invert:
            gs_img = ImageChops.invert(gs_img)
        out_ascii = self.to_ascii_chars(gs_img)

        with open(self.out_file, 'w') as file:
            file.write(out_ascii)

        return out_ascii


def get_result_image():
    parser = parse.ParserArguments()
    img_file, out_file, width, height, invert, contrast = parser.parse()

    converter = ImageConverter(img_file, out_file, width,
                               height, invert, contrast)
    converter.convert()


def main():
    get_result_image()


if __name__ == '__main__':
    main()
