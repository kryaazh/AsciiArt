#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageChops, ImageStat
import numpy as np
from asciiart import ImageConverter
import CharDictionary as chars
import unittest


class TestConverter(unittest.TestCase):
    def test_resize(self):
        converter = ImageConverter(
            img_file=Image.open('img_for_test/black.jpg'),
            out_file='img_for_test/black.txt',
            arg_width=1,
            arg_height=1,
            arg_contrast=100,
            arg_invert=False)
        resized_image = converter.resize(converter.img, 100, 100)
        new_width, new_height = resized_image.size
        converter.img.close()
        self.assertEqual((100, 100), (new_width, new_height))

    def test_get_size_in_blocks(self):
        converter = ImageConverter(
            img_file=Image.open('img_for_test/black.jpg'),
            out_file='img_for_test/black.txt',
            arg_width=1,
            arg_height=1,
            arg_contrast=100,
            arg_invert=False)
        converter.img.close()
        img = Image.new('L', (14, 14))

        self.assertEqual(converter.get_size_in_blocks(img), (2, 1))

    def test_get_most_suitable_char(self):
        converter = ImageConverter(
            img_file=Image.open('img_for_test/black.jpg'),
            out_file='img_for_test/black.txt',
            arg_width=1,
            arg_height=1,
            arg_contrast=100,
            arg_invert=False)
        char = converter.get_most_suitable_char(converter.img, 1, 1)
        converter.img.close()
        self.assertEqual(char, "W")

    def test_to_ascii_char(self):
        converter = ImageConverter(
            img_file=Image.open('img_for_test/black.jpg'),
            out_file='img_for_test/black.txt',
            arg_width=1,
            arg_height=1,
            arg_contrast=100,
            arg_invert=False)
        ascii_img = converter.to_ascii_chars(converter.img)
        converter.img.close()
        self.assertEqual(ascii_img, "W")

    def test_convert(self):
        converter = ImageConverter(
            img_file=Image.open('img_for_test/black.jpg'),
            out_file='img_for_test/black.txt',
            arg_width=1,
            arg_height=1,
            arg_contrast=100,
            arg_invert=False)
        img = converter.convert()
        converter.img.close()
        self.assertEqual(img, "W")

    def test_to_gray_scale(self):
        converter = ImageConverter(
            img_file=Image.open('img_for_test/black.jpg'),
            out_file='img_for_test/black.txt',
            arg_width=1,
            arg_height=1,
            arg_contrast=100,
            arg_invert=False)

        img = converter.to_gray_scale(converter.img)

        img_arr = np.array([
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

        converter.img.close()
        self.assertEqual((img == img_arr).all(), True)


class TestCharDictionary(unittest.TestCase):
    def test_get_char_arr(self):
        char_dict = chars.CharDictionary()
        char = char_dict.get_char_arr(' ')

        char_arr = np.array([[255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255],
                             [255, 255, 255, 255, 255, 255, 255]])
        equal_arr = (char == char_arr).all()

        self.assertEqual(equal_arr, True)


if __name__ == "__main__":
    unittest.main()
