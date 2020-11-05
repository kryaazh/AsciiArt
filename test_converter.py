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
        resized_image = converter.resize(np.array(img), 100, 100)
        new_width, new_height = resized_image.shape[0], resized_image.shape[1]
        img.close()
        self.assertEqual((100, 100), (new_width, new_height))

    def test_get_size_in_blocks(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        img = Image.new('L', (14, 14))
        self.assertEqual(converter.get_size_in_blocks(np.array(img)), (2, 1))

    def test_get_most_suitable_char(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        img = Image.open('img_for_test/black.jpg')
        char = converter.get_most_suitable_char(np.array(img), 1, 1)
        img.close()
        self.assertEqual(char, "W")

    def test_to_ascii_char(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        img = Image.open('img_for_test/black.jpg')
        r_img = converter.resize(np.array(img),
                                 converter.width * 7,
                                 converter.height * 14)
        ascii_img = converter.to_ascii_chars(r_img)
        img.close()
        self.assertEqual(ascii_img, "W")

    def test_convert(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        img = Image.open('img_for_test/black.jpg')
        a_img = converter.convert(img)
        img.close()
        self.assertEqual(a_img, "W")

    def test_to_gray_scale(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=100, invert=False)

        image = Image.open('img_for_test/black.jpg')
        r_img = converter.resize(np.array(image),
                                 converter.width,
                                 converter.height)
        img = converter.to_gray_scale(r_img)
        img_arr = np.zeros((13, 26), dtype=np.int8)

        image.close()
        self.assertTrue((img == img_arr).all())

    def test_convert_diff_color(self):
        converter = ImageConverter(width=2, height=2,
                                   contrast=0, invert=False)
        image = Image.open('img_for_test/bwg.jpg')
        a_img = converter.convert(image)
        image.close()
        self.assertEqual(a_img, "Wj\n. ")

    def test_convert_more_diff_color(self):
        converter = ImageConverter(width=4, height=4,
                                   contrast=0, invert=False)
        image = Image.open('img_for_test/bwg.jpg')
        a_img = converter.convert(image)
        image.close()
        self.assertEqual(a_img, "WWjj\nWWjj\n..  \n..  ")

    def test_lines(self):
        converter = ImageConverter(width=2, height=2,
                                   contrast=0, invert=False)
        image = Image.open('img_for_test/lines.jpg')
        a_img = converter.convert(image)
        image.close()
        self.assertEqual(a_img, "Lr\n|j")

    def test_invert(self):
        converter = ImageConverter(width=1, height=1,
                                   contrast=0, invert=True)

        image = Image.open('img_for_test/E.jpg')
        a_img = converter.convert(image)
        image.close()
        self.assertEqual(a_img, "}")


class TestCharDictionary(unittest.TestCase):
    def test_get_char_arr(self):
        char_dict = chars.CharDictionary()
        char = char_dict.get_char_arr(' ')
        char_arr = 255 * np.ones((14, 7), dtype=np.int8)
        self.assertTrue((char == char_arr).all())


if __name__ == "__main__":
    unittest.main()
