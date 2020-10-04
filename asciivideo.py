#!/usr/bin/env python
import cv2
import shutil
import asciiart
import ParserArguments as parser
import sys
from PIL import Image, ImageChops


class AsciiVideo:
    @staticmethod
    def convert(input_img, w, h):
        _img = ImageChops.invert(input_img)
        resize_img = converter.resize(_img, w * asciiart.BLOCK_WIDTH - 1,
                                      h * asciiart.BLOCK_HEIGHT)
        gs_img = resize_img.convert('L')
        contrast_img = converter.change_contrast(gs_img, converter.contrast)
        return converter.to_ascii_chars(contrast_img)

    @staticmethod
    def get_image_from_camera():
        ret, frame = cam.read()
        if ret:
            return Image.fromarray(frame)
        return None

    @staticmethod
    def run_ascii_web_camera():
        while True:
            image = AsciiVideo.get_image_from_camera()
            (_width, _height) = shutil.get_terminal_size()
            sys.stdout.write(AsciiVideo.convert(image, _width, _height))


if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    (WIDTH, HEIGHT) = shutil.get_terminal_size()
    _parser = parser.ParserArguments()
    img_file, out_file, width, height, invert, contrast = _parser.parse()

    converter = asciiart.ImageConverter(width=WIDTH, height=HEIGHT,
                                        invert=invert, contrast=contrast)
    AsciiVideo.run_ascii_web_camera()
    cam.release()
    cv2.destroyAllWindows()

