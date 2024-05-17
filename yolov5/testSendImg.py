import cv2
import urllib.request
import numpy as np
import torch
import pathlib
import servor_command
import firebase_admin
from firebase_admin import credentials
import addTime

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
model = torch.hub.load('.', 'custom', path='last_5s_exp5.pt', source='local') 
# model = torch.hub.load('.', 'custom', path='runs/train/exp3/weights/best.pt', source='local') 
# model = torch.hub.load('.', 'custom', path='runs/train/exp3/weights/last.pt', source='local') 
# Replace the URL with the IP camera's stream URL
url = 'http://192.168.137.109/cam.jpg'
esp32_servor_ip = "192.168.137.53"

cred = credentials.Certificate("code/serviceAccountKey.json")
app = firebase_admin.initialize_app(cred, {
        'databaseURL': "https://ruypa-64600-default-rtdb.asia-southeast1.firebasedatabase.app/",
        'storageBucket': "ruypa-64600.appspot.com"
})

cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)


# Create a VideoCapture object
# cap = cv2.VideoCapture(url)
cap = cv2.VideoCapture(0)

# Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

# Read and display video frames
while True:
    success, img = cap.read()
    img1 = cv2.flip(img, 1) 
    # Rotate image 90 degrees clockwise
    img2 = cv2.rotate(img1, cv2.ROTATE_90_CLOCKWISE)

    # Resize img2 to match img1 dimensions
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Concatenate images horizontally
    combined_img = cv2.hconcat([img1, img2_resized])

    results = model(combined_img)
    r_img = results.render() # returns a list with the images as np.array
    img_with_boxes = r_img[0] # image with boxes as np.array


    class_counts = results.pandas().xyxy[0].value_counts('name')
    if not class_counts.empty:  # Kiểm tra xem đối tượng Series có rỗng không
        max_class = class_counts.idxmax()  # Lấy ra tên lớp có số lượng lớn nhất
        max_count = class_counts.max()     # Lấy ra số lượng lớn nhất
        if(max_class == "lipsticks"):
            print("true lipsticks")
            # servor_command.send_command(esp32_servor_ip, "90", 0.0)
            addTime.addAttendanceTime("LIPSTICK", img_with_boxes)
        if(max_class == "glasses"):
            print("true glasses") 
            # servor_command.send_command(esp32_servor_ip, "120", 0.0)
            addTime.addAttendanceTime("GLASSES", img_with_boxes)
        if(max_class == "sunscreen"):
            print("true sunscreen")
            # servor_command.send_command(esp32_servor_ip, "60", 0.0)
            addTime.addAttendanceTime("SUNSCREEN", img_with_boxes)

    cv2.imshow('live Cam Testing',img_with_boxes)
    key=cv2.waitKey(1)
    if key==ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()