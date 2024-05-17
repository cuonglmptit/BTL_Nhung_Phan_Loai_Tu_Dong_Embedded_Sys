import torch
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
model = torch.hub.load('.', 'custom', path='best_5m_exp6.pt', source='local') 
import time
import cv2
import servor_command
esp32_servor_ip = "192.168.137.205"

# Initialize the webcam
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

old = ""

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) 
    results = model(img)
    r_img = results.render() # returns a list with the images as np.array
    img_with_boxes = r_img[0] # image with boxes as np.array
    class_counts = results.pandas().xyxy[0].value_counts('name')
    # if not class_counts.empty:  # Kiểm tra xem đối tượng Series có rỗng không
    #     max_class = class_counts.idxmax()  # Lấy ra tên lớp có số lượng lớn nhất
    #     max_count = class_counts.max()     # Lấy ra số lượng lớn nhất
    #     if(max_class == "lipsticks"):
    #         print("true lipsticks")
    #         servor_command.send_command(esp32_servor_ip, "90", 1)
    #     if(max_class == "glasses"):
    #         print("true glasses")
    #         servor_command.send_command(esp32_servor_ip, "180", 1)
    #     if(max_class == "sunscreen"):
    #         print("true sunscreen")
    #         servor_command.send_command(esp32_servor_ip, "0", 1)
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()