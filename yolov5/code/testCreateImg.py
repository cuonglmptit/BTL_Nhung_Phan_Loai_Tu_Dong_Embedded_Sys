import cv2
import numpy as np
import matplotlib.pyplot as plt

# Tạo một ảnh màu 256x256 với giá trị từ 0 đến 255
height, width = 256, 256
image = np.zeros((height, width, 3), dtype=np.uint8)

# Tạo màu nền xanh lá cây
image[:] = [0, 255, 0]  # Màu xanh lá cây

# Vẽ một hình tròn màu đỏ ở giữa ảnh
cv2.circle(image, (height//2, width//2), height//4, (255, 0, 0), -1)

# Hiển thị ảnh
plt.imshow(image)
plt.title('RGB Image')
plt.axis('off')
plt.show()