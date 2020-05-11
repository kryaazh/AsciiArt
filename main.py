#!/usr/bin/env python

import argparse
import math
import sys
import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageChops, ImageStat

chars = np.array([' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                  'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                  'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                  'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                  'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#',
                  '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/',
                  ':', ';', '?', '@', '\\', '^', '_', '`', '{', '|', '}',
                  '~', '<', '=', '>'])

block_width = 13
block_height = 26


class ParserArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser(add_help=True, description="Image to ASCII")
        self.parser.add_argument('-i', '--input', dest='input_file', required=True)
        self.parser.add_argument('-o', '--output', dest='output_file', required=True)
        self.parser.add_argument('-b', '--background', dest="background_color", required=False, default="white")
        self.parser.add_argument('-x', '--width', dest='width', required=False, default=1000)
        self.parser.add_argument('-y', '--height', dest='height', required=False, default=1000)

    def parse(self):
        args = self.parser.parse_args()
        input_file = args.input_file
        output_file = args.output_file

        width = None
        if args.width is not None:
            width = int(args.width)

        height = None
        if args.height is not None:
            height = int(args.height)

        background_color = args.background_color

        return input_file, output_file, width, height, background_color


class CharDictionary:
    def __init__(self):
        self.char_dict = {}
        self.font = ImageFont.truetype("fonts\\RobotoMono-Regular.ttf", 20)
        self.counter = 0

    def get_char_img(self, char):
        char_img = Image.new('L', (int(block_width), int(block_height)), 255)
        drawer = ImageDraw.Draw(char_img)
        drawer.text((0, 0), char, font=self.font, fill=0)

        char_img.save(f'''char_dict\\{self.counter}.jpg''')
        return char_img

    def get_char_dict(self):
        files = os.listdir("char_dict")

        if not files:
            self.counter = 0
            for char in chars:
                char_img = self.get_char_img(char)
                self.char_dict[char] = char_img
                self.counter += 1
        else:
            self.counter = 0
            for char in chars:
                char_img = Image.open(f'''char_dict\\{self.counter}.jpg''')
                self.char_dict[char] = char_img
                self.counter += 1


def to_gray_scale(img):
    img_arr = np.array(img)
    gs_factors = np.array([0.2989, 0.587, 0.114])

    width, height = img_arr.shape[0], img_arr.shape[1]
    try:
        img_arr.reshape(width * height, 3)
        out = np.matmul(img_arr, gs_factors)
    except ValueError:
        return Image.fromarray(img_arr)

    return Image.fromarray(out.reshape(width, height))


class ImageConverter:
    def __init__(self, img_file, out_file, arg_width, arg_height, arg_background_color, arg_contrast_level):
        self.img = Image.open(img_file)
        self.out_file = out_file
        self.width, self.height = self.img.size
        self.arg_width = arg_width
        self.arg_height = arg_height
        self.background_color = arg_background_color
        self.contrast_level = arg_contrast_level

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
        count_block_w = math.floor(img.size[0] / block_width)
        count_block_h = math.floor(img.size[1] / block_height)

        return count_block_w, count_block_h

    @staticmethod
    def change_contrast(img, level):
        factor = (259 * (level + 255)) / (255 * (259 - level))

        def contrast(c):
            return 128 + factor * (c - 128)

        return img.point(contrast)

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

    @staticmethod
    def get_most_suitable_char(img, x, y):
        dict_creator = CharDictionary()
        dict_creator.get_char_dict()
        char_dict = dict_creator.char_dict
        min_diff = sys.maxsize
        most_suitable_char = " "
        next_x = x * block_width
        next_y = y * block_height
        block = img.crop((next_x, next_y, next_x + block_width, next_y + block_height))

        for char in char_dict:
            difference = ImageChops.difference(block, char_dict[char])
            statistic = ImageStat.Stat(difference)
            diff = statistic.sum[0]
            if diff < min_diff:
                min_diff = diff
                most_suitable_char = char
        return most_suitable_char

    def convert(self):
        if self.background_color == "white":
            bg_color_code = 255
        else:
            bg_color_code = 0

        font = ImageFont.truetype("fonts\\RobotoMono-Regular.ttf", 20)
        resize_img = self.resize(self.img, self.arg_width, self.arg_height)
        contrast_img = self.change_contrast(resize_img, 150)
        gs_img = contrast_img.convert('L')
        out_ascii = self.to_ascii_chars(gs_img)

        blocks_count_w, blocks_count_h = self.get_size_in_blocks(gs_img)
        out_width = block_width * blocks_count_w
        out_height = block_height * blocks_count_h

        out_image = Image.new('L', (out_width, out_height), bg_color_code)
        draw = ImageDraw.Draw(out_image)
        draw.text((0, 0), out_ascii, fill=255-bg_color_code, font=font)

        out_image.save(self.out_file)

        with open("last_ascii.txt", 'w') as file:
            file.write(out_ascii)


class VerifierArguments:
    def __init__(self, img_file, out_file, width, height):
        self.img_file = img_file
        self.out_file = out_file
        self.width = width
        self.height = height

    @staticmethod
    def verify_img(img):
        try:
            Image.open(img)
        except OSError:
            print('Входной файл не является изображением')


class ImageToAscii:
    parser = ParserArguments()
    img_file, out_file, width, height, background_color = parser.parse()
    verifier = VerifierArguments(img_file, out_file, width, height)
    verifier.verify_img(img_file)
    converter = ImageConverter(img_file, out_file, width, height, background_color)
    converter.convert()


def main():
    ImageToAscii()


if __name__ == '__main__':
    main()
