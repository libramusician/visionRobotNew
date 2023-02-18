import socket

import cv2

from receiver.CameraReceiver import CameraReceiver


class UDPsource():
    def __init__(self, camera: CameraReceiver):
        self.receiver = camera
        self.ip = "127.0.0.1"
        self.send_port = 6000
        self.receive_port = 8002
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.ip, self.send_port))
        self.s2.bind((self.ip, self.receive_port))
        print("waiting for connection")
        # wait for hello message

    def run(self):
        data, addr = self.s.recvfrom(1024)
        print("connection received")
        while True:
            # grab frame from camera
            frame = self.receiver.receive()
            # frame2 = cv2.resize(frame, (320, 240))
            ok, frame_bytes = cv2.imencode(".jpg", frame)
            print(len(frame_bytes))
            try:
                self.s.sendto(frame_bytes, addr)

                print("msg sent to " + str(addr))
                response, _ = self.s2.recvfrom(4)
                print("msg recv")
                print(response)
            except Exception as error:
                print(error)

    def clean_up(self):
        self.s.close()
        self.s2.close()


if __name__ == '__main__':
    r = UDPsource(CameraReceiver())
    try:
        r.run()
    except Exception as e:
        print(e)
    finally:
        r.clean_up()
