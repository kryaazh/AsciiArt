#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageChops, ImageStat
import numpy as np
from asciiart import ImageConverter
import CharDictionary as chars
import unittest


class TestConverter(unittest.TestCase):
    def test_resize(self):
        converter = ImageConverter(img_file='img_for_test/jer.jpg',
                                   out_file='img_for_test/jer_r.jpg',
                                   arg_width=200,
                                   arg_height=100,
                                   arg_contrast=100,
                                   arg_invert=False)
        img = Image.open('img_for_test/resized_jer.jpg')

        resized_image = converter.resize(img, 100, 100)
        new_width, new_height = resized_image.size

        self.assertEqual((100, 100), (new_width, new_height))

    def test_get_size_in_blocks(self):
        img = Image.new('L', (14, 14))

        self.assertEqual(ImageConverter.get_size_in_blocks(img), (2, 1))

    def test_get_most_suitable_char(self):
        converter = ImageConverter(img_file='img_for_test/jer.jpg',
                                   out_file='img_for_test/jer_r.jpg',
                                   arg_width=200,
                                   arg_height=100,
                                   arg_contrast=100,
                                   arg_invert=False)
        img = Image.open("img_for_test/black.jpg")

        self.assertEqual(converter.get_most_suitable_char(img, 1, 1), "W")

    def test_to_ascii_char(self):
        converter = ImageConverter(img_file='img_for_test/black.jpg',
                                   out_file='img_for_test/black.txt',
                                   arg_width=13,
                                   arg_height=26,
                                   arg_contrast=100,
                                   arg_invert=False)

        ascii_img = Image.new('L', converter.img.size)
        draw = ImageDraw.Draw(ascii_img)
        draw.text((0, 0), "W")

        img = converter.to_ascii_chars(converter.img)
        result_img = Image.new('L', converter.img.size)
        draw = ImageDraw.Draw(result_img)
        draw.text((0, 0), img)

        difference = ImageChops.difference(result_img, ascii_img)
        statistic = ImageStat.Stat(difference)
        diff = statistic.sum[0]

        self.assertEqual(diff, 0)

    def test_convert(self):
        converter = ImageConverter(img_file='img_for_test/black.jpg',
                                   out_file='img_for_test/black.txt',
                                   arg_width=13,
                                   arg_height=26,
                                   arg_contrast=100,
                                   arg_invert=False)

        img = converter.convert()
        self.assertEqual(img, "W")

    def test_to_gray_scale(self):
        converter = ImageConverter(img_file='img_for_test/black.jpg',
                                   out_file='img_for_test/black.txt',
                                   arg_width=13,
                                   arg_height=26,
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
