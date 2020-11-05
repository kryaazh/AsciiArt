#!/usr/bin/env python
import sys
import cv2
import numpy as np
from PIL import Image
import argparse

CHARS = dict(enumerate(' 0123456789'
                       'abcdefghijklmnopqrstuvwxyz'
                       'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                       '!"#$%&()*+,-./:;?@\\^_`{|}~<=>'))


class ImageConverter:
    CHAR_DICT = np.load("chars/chars.npy")
    BLOCK_WIDTH = 7
    BLOCK_HEIGHT = 14

    def __init__(self, width, height, invert, contrast):
        self.width = width
        self.height = height
        self.invert = invert
        self.contrast = contrast

    @staticmethod
    def resize(img, width, height):
        _new_width = 0
        _new_height = 0
        _width, _height = img.shape[1], img.shape[0]
        ratio = _height / _width

        if width and height:
            _new_width = width
            _new_height = height
        elif not width and not height:
            _new_width = 120
            _new_height = ratio * _new_width
        elif width and not height:
            _new_width = width
            _new_height = ratio * width
        elif height and not width:
            _new_height = height
            _new_width = height / ratio

        return cv2.resize(np.array(img), (int(_new_width), int(_new_height)))

    def get_size_in_blocks(self, img):
        return int(img.shape[1] / self.BLOCK_WIDTH),\
               int(img.shape[0] / self.BLOCK_HEIGHT)

    @staticmethod
    def change_contrast(img, level):
        f = 131 * (level + 127) / (127 * (131 - level))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(img, alpha_c, img, 0, gamma_c)
        return buf

    @staticmethod
    def to_gray_scale(img_arr):
        gs_factors = np.array([0.2989, 0.587, 0.114])
        width, height = img_arr.shape[1], img_arr.shape[0]
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
        next_x = x * self.BLOCK_WIDTH
        next_y = y * self.BLOCK_HEIGHT

        block = img[next_y:(next_y + self.BLOCK_HEIGHT),
                    next_x:(next_x + self.BLOCK_WIDTH)]

        for i in range(len(CHARS)):
            if self.invert:
                difference = np.sum(abs((254 - self.CHAR_DICT[i, :]) - block))
            else:
                difference = np.sum(abs(self.CHAR_DICT[i, :] - block))
            if difference < min_diff:
                min_diff = difference
                most_suitable_char = CHARS[i]
        return most_suitable_char

    def convert(self, img):
        gs_img = img.convert("L")
        resize_img = self.resize(np.array(gs_img),
                                 self.width * self.BLOCK_WIDTH,
                                 self.height * self.BLOCK_HEIGHT)
        contrast_img = self.change_contrast(resize_img, self.contrast)
        if self.invert:
            contrast_img = cv2.bitwise_not(contrast_img)

        return self.to_ascii_chars(contrast_img)


def parse():
    parser = argparse.ArgumentParser(add_help=True,
                                     description="Image to ASCII")
    parser.add_argument('-i', '--input', dest='input')
    parser.add_argument('-o', '--output', dest='output', required=False,
                        help="The picture file to be converted")
    parser.add_argument('-W', '--width', dest='width', required=False,
                        default=100, type=int,
                        help="The width of output in ascii chars")
    parser.add_argument('-H', '--height', dest='height', required=False,
                        default=100, type=int,
                        help="The height of output in ascii chars")
    parser.add_argument('--invert', dest="invert", required=False,
                        action='store_true',
                        help="Convert an inverted image")
    parser.add_argument('-c', '--contrast', dest='contrast', required=False,
                        default=0, type=int,
                        help="Changes the contrast of the image, "
                             "allowed values [-127; 127]")

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    width = args.width
    height = args.height
    contrast = args.contrast
    invert = args.invert

    return input_file, output_file, width, height, invert, contrast


def get_result_image():
    img_file, out_file, width, height, invert, contrast = parse()
    converter = ImageConverter(width, height, invert, contrast)
    ascii_image = converter.convert(Image.open(img_file))

    if not out_file:
        sys.stdout.write(ascii_image)
    else:
        with open(out_file, 'w') as file:
            file.write(ascii_image)


def main():
    get_result_image()


if __name__ == '__main__':
    main()
