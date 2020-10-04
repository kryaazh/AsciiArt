#!/usr/bin/env python
from PIL import Image
import numpy as np
from asciiart import ImageConverter
import CharDictionary as chars
import unittest


class TestConverter(unittest.TestCase):
    def test_resize(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)
        img = Image.open('img_for_test/black.jpg')
        resized_image = converter.resize(img, 100, 100)
        new_width, new_height = resized_image.size
        img.close()
        self.assertEqual((100, 100), (new_width, new_height))

    def test_get_size_in_blocks(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        img = Image.new('L', (14, 14))
        self.assertEqual(converter.get_size_in_blocks(img), (2, 1))

    def test_get_most_suitable_char(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        img = Image.open('img_for_test/black.jpg')
        char = converter.get_most_suitable_char(img, 1, 1)
        img.close()
        self.assertEqual(char, "W")

    def test_to_ascii_char(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        img = Image.open('img_for_test/black.jpg')
        r_img = converter.resize(img,
                                 converter.width * 7,
                                 converter.height * 14)
        ascii_img = converter.to_ascii_chars(r_img)
        img.close()
        self.assertEqual(ascii_img, "W")

    def test_convert(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        img = Image.open('img_for_test/black.jpg')
        a_img = converter.convert(img, 'img_for_test/black.txt')
        img.close()
        self.assertEqual(a_img, "W")

    def test_to_gray_scale(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        image = Image.open('img_for_test/black.jpg')
        r_img = converter.resize(image,
                                 converter.width,
                                 converter.height)
        img = converter.to_gray_scale(r_img)

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

        image.close()
        self.assertTrue((img == img_arr).all())


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

        self.assertTrue(equal_arr)


if __name__ == "__main__":
    unittest.main()
