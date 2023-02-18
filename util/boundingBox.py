import cv2
import numpy

GREEN = (0, 255, 0)
THICKNESS = 2
IOU_THRESHOLD = 0.5


def get_center_from_box(box: tuple[int, int, int, int]):
    """
    This function is to
    get the center position of a box
    with the format (x,y,w,h)
    :param box: bounding box with the format (x,y,w,h)
    :return: the center with format (x, y)
    """
    return (box[0] + box[2] / 2), (box[1] + box[3] / 2)

def draw(bbox, frame: numpy.ndarray):
    """
    This function is to
    take the bounding box on frame
    in the given bounding box and frame.
    :param bbox: Bounding box
    :param frame: Frame to draw
    """
    x = bbox[0]
    y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, thickness=THICKNESS)


class BoundingBox:
    def __init__(self, bbox):
        """
        This function is to
        initial bounding box values.
        They are upper left corner coordinate,
        weight, height, color and thickness of the bounding box.
        :param bbox: Bounding box
        """
        self.x = bbox[0]
        self.y = bbox[1]
        self.w = bbox[2]
        self.h = bbox[3]
        self.color = GREEN
        self.thickness = THICKNESS

    def get_center(self):
        """
        This function is to
        get the center position of this bounding box
        within the bounding box.
        :return: Center of bounding box
        """
        return (self.x + self.w / 2), (self.y + self.h / 2)

    # def draw_on(self, frame: numpy.ndarray):
    #     cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), self.color, thickness=self.thickness)

    def get_xywh(self):
        """
        This function is to get
        the bounding box x and y values which are the upper left corner coordinate of bounding box,
        width and height of bounding box.
        :return:
        """
        return self.x, self.y, self.w, self.h

    def set_xywh(self, x, y, w, h):
        """
        This function is to set up
        the bounding box x and y values which are the upper left corner coordinate of bounding box,
        width and height of bounding box.
        :param x: x value of upper left corner coordinate in the bounding box
        :param y: y value of upper left corner coordinate in the bounding box
        :param w: width value of the bounding box
        :param h: height value of the bounding box
        :return:
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def is_tracked_by(self, trackers, frame):
        """
        This function is to  find out
        the tracker that tracks the current bounding box

        :param trackers: All current trackers
        :param frame: frame to draw
        :return:None or the most suitable tracker
        """

        confidences = {}
        print(trackers)
        for tracker in trackers:
            ok, bbox = tracker.update(frame)
            iou_ratio = iou(self, BoundingBox(bbox))
            confidences[iou_ratio] = tracker
            # TODO: simple, use max to be more accurate
        if len(confidences) == 0:
            return None
        else:
            best = max(confidences)
            if best > IOU_THRESHOLD:
                return confidences[best]
            else:
                return None


def iou(a: BoundingBox, b: BoundingBox):
    """
    Calculate the intersection over union
    :param a: Bounding Box Class
    :param b: Bounding Box Class
    :return: Intersection over union
    """
    area_a = a.w * a.h
    area_b = b.w * b.h
    w = min(b.x + b.w, a.x + a.w) - max(a.x, b.x)
    h = min(b.y + b.h, a.y + a.h) - max(a.y, b.y)
    if w <= 0 or h <= 0:
        return 0
    area_c = w * h
    return area_c / (area_a + area_b - area_c)
