#!/usr/bin/env python

import cv2
import asciiart
import sys
import os
from PIL import Image, ImageChops

cam = cv2.VideoCapture(0)
converter = asciiart.ImageConverter('img_for_test/jer.jpg',
                                    'img_for_test/jer.txt',
                                    100, 100, True, 200)


def convert(input_img):
    img = Image.fromarray(input_img)
    img = ImageChops.invert(img)
    resize_img = converter.resize(img, 280, 280)
    gs_img = resize_img.convert('L')
    gs_img = converter.change_contrast(gs_img, 80)

    return converter.to_ascii_chars(gs_img)


while True:
    ret, frame = cam.read()
    if not ret:
        break
    k = cv2.waitKey(1)

    ascii_img = convert(frame)

    os.system("cls")
    sys.stdout.write('\r' + ascii_img)

cam.release()
cv2.destroyAllWindows()
