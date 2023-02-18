import cv2
from receiver.UDPReceiver import UDPReceiver
from util.UDPSender import UDPSender

ip = "127.0.0.1"
ctr_addr = (ip, 8002)
frame_addr = (ip, 6000)

receiver = UDPReceiver()
sender = UDPSender(ctr_addr)

# for UDP only
receiver.connect(frame_addr)

counter = 1

while True:
    # Capture frame-by-frame
    frame = receiver.receive()
    if frame is None:
        continue
    sender.send("0")

    # Display the resulting frame
    cv2.imshow('Webcam', frame)

    # Wait for the user to press a key
    key = cv2.waitKey(1) & 0xFF

    # If the 's' key is pressed, save the image to disk
    if key == ord('s'):
        cv2.imwrite(f'captured_image{counter}.png', frame)
        counter += 1
        print("Image saved!")
    elif key == ord('q'):
        break

# Release the webcam and close the window
cv2.destroyAllWindows()
