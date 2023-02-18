import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Set the image size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
counter = 1

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

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
cap.release()
cv2.destroyAllWindows()
