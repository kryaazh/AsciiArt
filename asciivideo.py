#!/usr/bin/env python

import cv2
import asciiart
import sys
import os
from PIL import Image, ImageChops

cam = cv2.VideoCapture(0)
# cv2.namedWindow("test")

img_counter = 0
converter = asciiart.ImageConverter('img_for_test/jer.jpg',
                                    'img_for_test/jer.txt',
                                    100, 100, True, 200)

while True:
    ret, frame = cam.read()
    # cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    img = Image.fromarray(frame)
    img = ImageChops.invert(img)
    resize_img = converter.resize(img, 400, 400)
    gs_img = resize_img.convert('L')
    ascii_img = converter.to_ascii_chars(gs_img)

    os.system("cls")
    sys.stdout.write('\r' + ascii_img)

    if k % 256 == 27:
        print("Escape hit, closing...")
        break

cam.release()
