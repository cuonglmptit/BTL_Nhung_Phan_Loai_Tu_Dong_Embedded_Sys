import os
import cv2
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

import numpy as np
import addTime

def test():
    cred = credentials.Certificate("?serviceAccountKey.json")
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': "https://?.asia-southeast1.firebasedatabase.app/",
        'storageBucket': "?.appspot.com"
    })


    # lấy biến hình ảnh ở đây

    height, width = 256, 256
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Set background color to green
    image[:] = [0, 255, 0]  # Green color

    # Draw a red circle in the center
    cv2.circle(image, (height // 2, width // 2), height // 4, (255, 0, 0), -1)



    # addTime.addAttendanceTime("LIPSTICK", image)

    # addTime.addAttendanceTime("SUNSCREEN", image)

    addTime.addAttendanceTime("GLASSES", image)

test()
