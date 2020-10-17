#!/usr/bin/env python
import argparse
from PIL import Image


class ParserArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser(add_help=True,
                                              description="Image to ASCII")
        self.parser.add_argument('-i', '--input', dest='input')
        self.parser.add_argument('-o', '--output', dest='output',
                                 required=False)
        self.parser.add_argument('-W', '--width', dest='width',
                                 required=False, default=100)
        self.parser.add_argument('-H', '--height', dest='height',
                                 required=False, default=100)
        self.parser.add_argument('--invert', dest="invert",
                                 required=False, action='store_true')
        self.parser.add_argument('-c', '--contrast', dest='contrast',
                                 required=False, default=0)

    def parse(self):
        args = self.parser.parse_args()

        input_file = args.input

        output_file = None
        if args.output is not None:
            output_file = args.output

        width = None
        if args.width is not None:
            width = int(args.width)

        height = None
        if args.height is not None:
            height = int(args.height)

        contrast = int(args.contrast)
        invert = args.invert

        return input_file, output_file, width, height, invert, contrast


if __name__ == "__main__":
    ParserArguments()
