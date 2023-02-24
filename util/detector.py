import cv2.aruco
import numpy
from numpy.lib.npyio import NpzFile
import util.logger as logger
from util.rootFinder import rel_path_2_abs

path = rel_path_2_abs("calibration/camera_calibration.npz")
data: NpzFile = numpy.load(path)
mtx = data['mtx']
dist = data['dist']
rvecs = data['rvecs']
tvecs = data['tvecs']

# need measure, in cm
MARKER_SIZE = 16

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
    x, y, w, h, also the depth
    :param frame: the raw frame
    :return: true if detected, then provide the bounding box in form of x, y, w, h and depth.
             false if not detected and provide None
    """
    detector = cv2.aruco.ArucoDetector()
    marker_corners, _, _ = detector.detectMarkers(frame)
    # marker_corners, _, _ = cv2.aruco.detectMarkers(frame, dictionary)
    if len(marker_corners) > 0:
        depth = get_depth(marker_corners)
        x1 = int(marker_corners[0][0][0][0])
        y1 = int(marker_corners[0][0][0][1])
        x2 = int(marker_corners[0][0][2][0])
        y2 = int(marker_corners[0][0][2][1])
        cv2.rectangle(frame,
                      (x1, y1),
                      (x2, y2),
                      (255, 0, 0), thickness=2)
        return True, (x1, y1, (x2 - x1), (y2 - y1)), depth
    else:
        return False, None, None


# @logger.add_log
def get_depth(marker_corners):
    _, tv, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, MARKER_SIZE, cameraMatrix=mtx, distCoeffs=dist)
    # tv contains x,y,z of the marker, marker id 0, first detected, and depth is 2
    return tv[0][0][2]
