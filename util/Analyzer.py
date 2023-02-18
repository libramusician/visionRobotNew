import numpy

from util import boundingBox

REGION_L1 = 0.45
REGION_R1 = 0.55


def analysis(bbox: tuple[int, int, int, int], frame: numpy.ndarray):
    width = frame.shape[1]
    x, y = boundingBox.get_center_from_box(bbox)
    if 0 <= x < width * REGION_L1:
        return "5"
    elif width * REGION_L1 <= x < width * REGION_R1:
        return "0"
    else:
        return "6"
