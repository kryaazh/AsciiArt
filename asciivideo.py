#!/usr/bin/env python
import cv2
import shutil
import asciiart
import sys
from PIL import Image, ImageChops

cam = cv2.VideoCapture(0)
(WIDTH, HEIGHT) = shutil.get_terminal_size()
converter = asciiart.ImageConverter(width=WIDTH, height=HEIGHT,
                                    invert=True, contrast=80)


def convert(input_img, w, h):
    _img = ImageChops.invert(input_img)
    resize_img = converter.resize(_img, w * asciiart.BLOCK_WIDTH - 1,
                                  h * asciiart.BLOCK_HEIGHT)
    gs_img = resize_img.convert('L')
    contrast_img = converter.change_contrast(gs_img, converter.contrast)
    return converter.to_ascii_chars(contrast_img)


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

