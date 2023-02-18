import argparse
import asyncio
import base64

import cv2
import websockets
from receiver.CameraReceiver import CameraReceiver
from receiver.UDPReceiver import UDPReceiver
from util.UDPSender import UDPSender
from util import detector
from util import Analyzer
import global_variable

import client

observers = set()
current_frame_str = ""



async def handle_client(websocket, path):
    print("send task created")
    new_client = client.Client(websocket)
    observers.add(new_client)
    print("send task created")

    try:
        while True:
            global_variable.command = await websocket.recv()
    except websockets.ConnectionClosed:
        print("connection closed")
        observers.remove(new_client)
    # finally:
    #     send_task.cancel()


async def process_frames(ip):
    ctr_addr = (ip, 8002)
    frame_addr = (ip, 6000)
    # cam = CameraReceiver()
    receiver = UDPReceiver()
    sender = UDPSender(ctr_addr)

    # for UDP only
    receiver.connect(frame_addr)
    while True:
        frame = receiver.receive()
        if frame is None:
            continue
        detected, result = detector.detect(frame)
        final_cmd = "0"
        # user sent a command, change final command and clear set command
        if global_variable.command != final_cmd:
            final_cmd = global_variable.command
            global_variable.command = "0"
        # set command is "0", try if there is detection
        else:
            if detected:
                final_cmd = Analyzer.analysis(result, frame)

        # send final command back to robot
        print(final_cmd)
        sender.send(final_cmd)

        # send frame to user
        ok, frame_bytes = cv2.imencode(".jpg", frame)
        frame_str = base64.b64encode(frame_bytes.tobytes())
        print(frame_str)
        obs: client.Client
        for obs in observers:
            await obs.response(frame_str)

        # give some time for send buffer to flush
        await asyncio.sleep(0.03)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()


async def main(ip):
    asyncio.create_task(process_frames(ip))

    async with websockets.serve(handle_client, 'localhost', 50000):
        print('Server started, waiting for clients...')
        try:
            await asyncio.Future()  # run indefinitely
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", default="127.0.0.1")
    args = parser.parse_args()

    asyncio.run(main(args.ip))
