#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageChops, ImageStat
from asciiart import ImageConverter, VerifierArguments
import unittest


class TestConverter(unittest.TestCase):
    def test_resize(self):
        converter = ImageConverter(img_file='img_for_test/jer.jpg',
                                   out_file='img_for_test/jer_r.jpg',
                                   arg_width=200,
                                   arg_height=100,
                                   arg_background_color="white",
                                   arg_contrast=100)
        img = Image.open('img_for_test/resized_jer.jpg')

        resized_image = converter.resize(img, 100, 100)
        new_width, new_height = resized_image.size

        self.assertEqual((100, 100), (new_width, new_height))

    def test_get_size_in_blocks(self):
        img = Image.new('L', (26, 26))

        self.assertEqual(ImageConverter.get_size_in_blocks(img), (2, 1))

    def test_get_most_suitable_char(self):
        img = Image.open("img_for_test/black.jpg")

        self.assertEqual(ImageConverter.get_most_suitable_char(img, 1, 1), "W")

    def test_to_ascii_char(self):
        converter = ImageConverter(img_file='img_for_test/black.jpg',
                                   out_file='img_for_test/black.jpg',
                                   arg_width=13,
                                   arg_height=26,
                                   arg_background_color="white",
                                   arg_contrast=100)

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


class TestVerify(unittest.TestCase):
    def test_true_verify(self):
        verifier = VerifierArguments(img_file='img_for_test/jer.jpg',
                                     out_file='img_for_test/jer_r.jpg')
        if verifier.verify_img(verifier.img_file):
            ver = True
        else:
            ver = False

        self.assertEqual(ver, True)

    def test_false_verify(self):
        verifier = VerifierArguments(img_file='img_for_test/jer.txt',
                                     out_file='img_for_test/jer_r.jpg')

        if verifier.verify_img(verifier.img_file):
            ver = True
        else:
            ver = False

        self.assertEqual(ver, False)


if __name__ == "__main__":
    unittest.main()
