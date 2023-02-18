import cv2.aruco
import numpy

import util.fps as fps

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
# dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)


def generate_marker():
    # 200 x 200, 0 - 255
    maker_buffer = numpy.zeros((200, 200), dtype=numpy.uint8)
    marker = cv2.aruco.generateImageMarker(dictionary, 0, 200, img=maker_buffer, borderBits=1)
    cv2.imwrite("marker.png", marker)


@fps.add_fps
# @logger.add_log
def detect(frame):
    """
    try to detect the marker on the frame, if detected, draw and return the bounding box with format
    x, y, w, h
    :param frame: the raw frame
    :return: the bounding box in form of x, y, w, h
    """
    marker_corners, _, _ = cv2.aruco.ArucoDetector.detectMarkers(frame, dictionary)
    if len(marker_corners) > 0:
        x1 = int(marker_corners[0][0][0][0])
        y1 = int(marker_corners[0][0][0][1])
        x2 = int(marker_corners[0][0][2][0])
        y2 = int(marker_corners[0][0][2][1])
        cv2.rectangle(frame,
                      (x1, y1),
                      (x2, y2),
                      (255, 0, 0), thickness=2)
        return True, (x1, y1, (x2 - x1), (y2 - y1))
    else:
        return False, None


# generate_marker()
# marker_detect()
