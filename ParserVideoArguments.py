import argparse
import ParserArguments as parser

class ParserVideoArguments:
    def __init__(self):
        self.image_parser = parser.ParserArguments()
        self.parser = argparse.ArgumentParser(add_help=True,
                                              description="Video_Arguments")
        self.parser.add_argument('--invert', dest="invert",
                                 required=False, action='store_true')
        self.parser.add_argument('-c', '--contrast', dest='contrast',
                                 required=False, default=0)
        self.parser.add_argument('--id', dest="id_cam", default=0)

    def parse(self):
        args = self.parser.parse_args()

        contrast = int(args.contrast)
        invert = args.invert
        id_cam = int(args.id_cam)
        return invert, contrast, id_cam

if __name__ == "__main__":
    ParserVideoArguments()