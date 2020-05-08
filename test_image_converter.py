#!/usr/bin/env python

import numpy as np
from PIL import Image
from main import ImageConverter


def test_resize():
    converter = ImageConverter(img_file='img_for_test/jer.jpg',
                               out_file='img_for_test/jer.txt',
                               arg_width=200,
                               arg_height=100)
    img = Image.open('img_for_test/resized_jer.jpg')
    width, height = img.size

    resized_image = converter.resize(converter.img, 200, 100)
    new_width, new_height = resized_image.size

    assert (width, height) == (new_width, new_height)
