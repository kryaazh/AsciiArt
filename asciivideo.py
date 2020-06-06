#!/usr/bin/env python

import cv2
import shutil
import asciiart
import sys
from PIL import Image, ImageChops

cam = cv2.VideoCapture(0)


def convert(input_img):
    _img = ImageChops.invert(input_img)
    resize_img = converter.resize(_img,
                                  converter.arg_width * asciiart.block_width-1,
                                  converter.arg_height * asciiart.block_height)
    gs_img = resize_img.convert('L')
    gs_img = converter.change_contrast(gs_img, converter.contrast)

    return converter.to_ascii_chars(gs_img)


def get_image_from_camera():
    ret, frame = cam.read()
    if ret:
        return frame
    return None


while True:
    image = get_image_from_camera()
    (w, h) = shutil.get_terminal_size()
    converter = asciiart.ImageConverter(Image.fromarray(image),
                                        out_file="out.txt",
                                        arg_width=w,
                                        arg_height=h,
                                        arg_invert=True,
                                        arg_contrast=80)
    sys.stdout.write("\r" + convert(converter.img))

cam.release()
cv2.destroyAllWindows()
