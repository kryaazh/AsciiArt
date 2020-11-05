import argparse
import ParserArguments as parser


class ParserVideoArguments:
    def __init__(self):
        self.image_parser = parser.ParserArguments()
        self.parser = argparse.ArgumentParser(add_help=True,
                                              description="Video_Arguments")
        self.parser.add_argument('--invert', dest="invert",
                                 required=False, action='store_true',
                                 help="Convert an inverted image")
        self.parser.add_argument('-c', '--contrast', dest='contrast',
                                 required=False, default=0,
                                 help="Changes the contrast of the image, "
                                      "allowed values [-255; 255]")
        self.parser.add_argument('-С', '--camera-id', dest="camera_id",
                                 default=0,
                                 help="The id of the webcam from which"
                                      " the image will be converted")

    def parse(self):
        args = self.parser.parse_args()

        contrast = int(args.contrast)
        invert = args.invert
        camera_id = int(args.camera_id)
        return invert, contrast, camera_id


if __name__ == "__main__":
    ParserVideoArguments()
