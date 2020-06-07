#!/usr/bin/env python
import cv2
import shutil
import asciiart
import sys
from PIL import Image, ImageChops

cam = cv2.VideoCapture(0)
(width, height) = shutil.get_terminal_size()
converter = asciiart.ImageConverter(arg_width=width,
                                    arg_height=height,
                                    arg_invert=True,
                                    arg_contrast=80)


def convert(input_img, w, h):
    _img = ImageChops.invert(input_img)
    resize_img = converter.resize(_img,
                                  w * asciiart.block_width-1,
                                  h * asciiart.block_height)
    gs_img = resize_img.convert('L')
    gs_img = converter.change_contrast(gs_img, converter.contrast)

    return converter.to_ascii_chars(gs_img)


def get_image_from_camera():
    ret, frame = cam.read()
    if ret:
        return Image.fromarray(frame)
    return None


def run_ascii_web_camera():
    while True:
        image = get_image_from_camera()
        (_width, _height) = shutil.get_terminal_size()

        sys.stdout.write(convert(image, _width, _height))


if __name__ == "__main__":
    run_ascii_web_camera()
    cam.release()
    cv2.destroyAllWindows()

