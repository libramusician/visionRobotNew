import numpy as np
import cv2

# Define the size of the chessboard used for calibration
board_size = (9, 6)

# Define the object points of the chessboard corners in real-world coordinates
objp = np.zeros((board_size[0]*board_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all the calibration images
obj_points = []  # 3d point in real world space
img_points = []  # 2d points in image plane

# Get a list of calibration images
calibration_images = []
for i in range(4):
    f_name = f'captured_image{i+1}.png'
    calibration_images.append(f_name)

# Loop through each calibration image
for image_file in calibration_images:
    # Load the image and convert it to grayscale
    img = cv2.imread(image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, board_size, None)

    # If corners are found, add object points and image points
    if ret == True:
        obj_points.append(objp)
        img_points.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, board_size, corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

# Calibrate the camera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# Save the calibration parameters to a file
np.savez('camera_calibration.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

# Print the calibration parameters
print("Camera matrix:")
print(mtx)
print("Distortion coefficients:")
print(dist)
