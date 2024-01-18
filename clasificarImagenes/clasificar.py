import cv2
import numpy as np
import os
import uuid

# Variables to store points and flags
first_point = None
second_point = None
drawing = False
rectangle_complete = False
color = (255, 0, 0)  # Default color is red
label = 1  # Default label is 1

# List to store all drawn boxes
boxes = []

# Generate a unique identifier
unique_id = uuid.uuid4().hex

# Construct the filename
filename = f"hard_hat_workers400_png.rf.{unique_id}.jpg"

# Open the file for writing
f = open(f'labels/hard_hat_workers400_png.rf.{unique_id}.txt', 'a')

def click_event(event, x, y, flags, params):
    global first_point, second_point, drawing, rectangle_complete, boxes, padded_img, f

    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:
            # First click
            first_point = (x, y)
            drawing = True
        elif not rectangle_complete:
            # Second click
            second_point = (x, y)
            rectangle_complete = True

            # Print coordinates to console
            print(f"First point: {first_point}, Second point: {second_point}")

            # Add the box to the list of boxes
            boxes.append(((first_point, second_point), color))

            # Reset the drawing and rectangle_complete flags for the next rectangle
            drawing = False
            rectangle_complete = False

            # Calculate the normalized coordinates
            x_center = (first_point[0] + second_point[0]) / 2 / 800
            y_center = (first_point[1] + second_point[1]) / 2 / 800
            width = abs(first_point[0] - second_point[0]) / 800
            height = abs(first_point[1] - second_point[1]) / 800

            # Append coordinates to the file with the current label
            with open(f'labels/hard_hat_workers400_png.rf.{unique_id}.txt', 'a') as f:
                f.write(f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    elif event == cv2.EVENT_MOUSEMOVE and drawing and not rectangle_complete:
        # Draw all the boxes with their colors
        img_temp = padded_img.copy()
        for box, box_color in boxes:
            cv2.rectangle(img_temp, box[0], box[1], box_color, 2)
        # Draw rectangle from first point to current mouse position
        cv2.rectangle(img_temp, first_point, (x, y), color, 2)
        cv2.imshow('image', img_temp)

# Load the image
img = cv2.imread('image.png', 1)

# Determine the longer side of the image
longer_side = max(img.shape[0], img.shape[1])

# Calculate the scaling factor
scale = 800 / longer_side

# Resize the image
resized_img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

# Determine the size of the padding
pad_y = (800 - resized_img.shape[0]) // 2
pad_x = (800 - resized_img.shape[1]) // 2

# Create a new image and copy the resized image into the center of it
padded_img = cv2.copyMakeBorder(resized_img, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

# Save the padded image with a unique name
filename = f"hard_hat_workers400.rf.{uuid.uuid4().hex}.jpg"
cv2.imwrite(os.path.join('images', filename), padded_img)

# Create a window and set the callback function
cv2.imshow('image', padded_img)
cv2.setMouseCallback('image', click_event)

# Wait for a key press and close the window if 'q' is pressed
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('h'):
        color = (0, 0, 255)  # Red color
        label = 0  # Label for 'h'
    elif key == ord('c'):
        color = (0, 255, 0)  # Green color
        label = 1  # Label for 'c'
    elif key == ord('q'):
        break

cv2.destroyAllWindows()