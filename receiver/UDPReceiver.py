import socket

import cv2
import numpy


class UDPReceiver:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.current_frame = None
        print("UDP receiver ready")

    def receive(self) -> numpy.ndarray:
        try:
            data, address = self.s.recvfrom(65536)

            # uncomment to skip size packet
            # data, address = self.s.recvfrom(1048576)

            frame_arr = numpy.array(bytearray(data))
            self.current_frame = cv2.resize(cv2.imdecode(frame_arr, cv2.IMREAD_UNCHANGED), (416, 416))
            return self.current_frame
        except Exception as e:
            print(e)
            print("connection stopped")
            exit(1)

    def connect(self, addr):
        self.s.sendto("hello".encode(), addr)

    def close(self):
        self.s.close()