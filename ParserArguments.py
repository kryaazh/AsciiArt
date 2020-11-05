#!/usr/bin/env python
import argparse
from PIL import Image


class ParserArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser(add_help=True,
                                              description="Image to ASCII")
        self.parser.add_argument('-i', '--input', dest='input')
        self.parser.add_argument('-o', '--output', dest='output',
                                 required=False,
                                 help="The picture file to be converted")
        self.parser.add_argument('-W', '--width', dest='width',
                                 required=False, default=100, type=int,
                                 help="The width of output in ascii chars")
        self.parser.add_argument('-H', '--height', dest='height',
                                 required=False, default=100, type=int,
                                 help="The height of output in ascii chars")
        self.parser.add_argument('--invert', dest="invert",
                                 required=False, action='store_true',
                                 help="Convert an inverted image")
        self.parser.add_argument('-c', '--contrast', dest='contrast',
                                 required=False, default=0, type=int,
                                 help="Changes the contrast of the image, "
                                      "allowed values [-255; 255]")

    def parse(self):
        args = self.parser.parse_args()

        input_file = args.input
        output_file = args.output
        width = args.width
        height = args.height
        contrast = args.contrast
        invert = args.invert

        return input_file, output_file, width, height, invert, contrast


if __name__ == "__main__":
    ParserArguments()
