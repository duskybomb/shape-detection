import cv2 as cv
from filled_shape import filled_shape as fs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--image", "-i", type=argparse.FileType('r'),
                    dest="image_path", help="Use image as source")
parser.add_argument("--cam", "-c", dest='cam', default=False, action='store_true', help="Use cam as source")
parser.add_argument("--debug", default=False, action='store_false', help="show more contours and points")

arg = parser.parse_args()

if arg.cam and arg.image_path is not None:
    raise Exception("Cam and Image cannot be used simultaneously")
if arg.cam:
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            fs.capture(frame, arg.debug)

        k = cv.waitKey(30) & 0xFF
        if k == 27:
            break
    cap.release()
    cv.destroyAllWindows()
elif arg.image_path is not None:
    frame = cv.imread(arg.image_path.name)
    fs.capture(frame, arg.debug)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    parser.parse_args(['--help'])

