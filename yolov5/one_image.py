import cv2
import urllib.request
import numpy as np
import torch
import pathlib
import servor_command

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
model = torch.hub.load('.', 'custom', path='last_5s_exp5.pt', source='local') 

# Read and display video frames
image_path = 'Untitled.jpg'

# Đọc ảnh từ file
img = cv2.imread(image_path)

# Kiểm tra xem ảnh có được đọc thành công không
if img is None:
    print("Không thể đọc ảnh từ đường dẫn đã cho.")
    exit()

results = model(img)
r_img = results.render() # returns a list with the images as np.array
img_with_boxes = r_img[0] # image with boxes as np.array

# Hiển thị ảnh trong cửa sổ
cv2.imshow('Image', img)

# Đợi người dùng nhấn phím bất kỳ để đóng cửa sổ
cv2.waitKey(0)

# Đóng tất cả các cửa sổ
cv2.destroyAllWindows()