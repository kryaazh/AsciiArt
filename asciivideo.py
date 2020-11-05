#!/usr/bin/env python
import cv2
import shutil
import asciiart
import argparse
import sys


def convert(input_img, w, h):
    img = cv2.bitwise_not(input_img)

    resize_img = converter.resize(img, w * converter.BLOCK_WIDTH - 1,
                                  h * converter.BLOCK_HEIGHT)
    contrast_img = converter.change_contrast(resize_img, converter.contrast)
    gs_img = cv2.cvtColor(contrast_img, cv2.COLOR_BGR2GRAY)

    if converter.invert:
        gs_img = cv2.bitwise_not(gs_img)

    return converter.to_ascii_chars(gs_img)


def get_image_from_camera():
    ret, frame = cam.read()
    if ret:
        return frame
    return None


def run_ascii_web_camera():
    while True:
        image = get_image_from_camera()
        (_width, _height) = shutil.get_terminal_size()
        sys.stdout.write(convert(image, _width, _height))


def parse():
    parser = argparse.ArgumentParser(add_help=True,
                                     description="Video_Arguments")
    parser.add_argument('--invert', dest="invert",
                        required=False, action='store_true',
                        help="Convert an inverted image")
    parser.add_argument('-c', '--contrast', dest='contrast',
                        required=False, default=0, type=int,
                        help="Changes the contrast of the image, "
                             "allowed values [-127; 127]")
    parser.add_argument('-С', '--camera-id', dest="camera_id",
                        default=0, type=int,
                        help="The id of the webcam from which"
                             " the image will be converted")
    args = parser.parse_args()
    return args.invert, args.contrast, args.camera_id


if __name__ == "__main__":
    invert, contrast, id_cam = parse()
    cam = cv2.VideoCapture(id_cam)
    (WIDTH, HEIGHT) = shutil.get_terminal_size()

    converter = asciiart.ImageConverter(width=WIDTH, height=HEIGHT,
                                        invert=invert, contrast=contrast)
    run_ascii_web_camera()
    cam.release()
    cv2.destroyAllWindows()
