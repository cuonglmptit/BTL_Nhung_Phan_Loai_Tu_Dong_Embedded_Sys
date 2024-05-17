import cv2
import urllib.request
import numpy as np

# Replace the URL with the IP camera's stream URL
url = 'http://192.168.137.109/cam.jpg'

cv2.namedWindow("Live Cam Testing", cv2.WINDOW_AUTOSIZE)

# Create a VideoCapture object
cap = cv2.VideoCapture(url)

# Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

# Read and display video frames
while True:
    # Read a frame from the video stream
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img1 = cv2.imdecode(imgnp, -1)
    # Rotate image 90 degrees clockwise
    img2 = cv2.rotate(img1, cv2.ROTATE_90_CLOCKWISE)

    # Resize img2 to match img1 dimensions
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Concatenate images horizontally
    combined_img = cv2.hconcat([img1, img2_resized])

    # Display the combined image
    cv2.imshow('Live Cam Testing', combined_img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
