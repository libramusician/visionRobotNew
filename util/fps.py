import time

import cv2

import global_variable


def add_fps(func):
    def wrapper(frame, *args, **kwargs):
        ret = func(frame, *args, **kwargs)
        fps = int(1 / (time.time() - global_variable.current_time))
        global_variable.current_time = time.time()
        cv2.putText(frame, str(fps), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
        return ret

    return wrapper
