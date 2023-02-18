import cv2

from receiver.CameraReceiver import CameraReceiver

class App:
    """
    fields:

    """
    def __init__(self, ip):
        self.ctraddr = (ip, 8002)
        self.frame_addr = (ip, 6000)
        self.receiver = CameraReceiver()
        # self.sender = UDPSender(self.ctraddr)
        # self.ui_sender = WSSender()
        # self.detector = AutoDetector()
        # self.trackers = []

        # states
        # self.single_tracker = None
        # self.mode_switch_counter = 0
        # self.detecting = Detecting(self)
        # self.tracking = Tracking(self)
        # self.single_tracking = SingleTracking(self)
        # self.single_detecting = SingleDetecting(self)
        # self.current_state = self.detecting
        # cv2.namedWindow("frame")
        # self.mouse_position = None
        # cv2.setMouseCallback("frame", self.mouse_clicked)

    # def mouse_clicked(self, event, x, y, flags, param):
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         print("mouse clicked")
    #         self.mouse_position = (x, y)
    #         print(self.mouse_position)
    #         self.current_state.mode_switch()

    def clean_up(self):
        cv2.destroyAllWindows()
        # self.receiver.close()
        # self.sender.close()

    def run(self):
        while True:
            frame = self.receiver.receive()

            detected, result = markerDetector.detect(frame)
            if not detected:
                self.sender.send("0")
            else:
                print(result)
                cmd = analysis(result)
                self.sender.send(cmd)

            ok, frame_bytes = cv2.imencode(".jpg", frame)

            frame_str = base64.b64encode(frame_bytes.tobytes())

            # asyncio.create_task(self.ui_sender.send(frame_str))
            asyncio.run(self.ui_sender.send(frame_str))

            cv2.imshow("frame", frame)
            if cv2.waitKey(16) == ord('q'):
                break