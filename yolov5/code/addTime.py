# import cv2
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from datetime import datetime

# import numpy as np


# def addAttendanceTime(id):


#     # Reference to the 'CLASSIFY' node in your database
#     ref = db.reference('CLASSIFY')

#     # Generate the current time as a string
#     new_attendance_time = str(datetime.now())

#     # Retrieve data for the 'LIPSTICK' child node
#     data_of_id = ref.child(id).get()

#     if not data_of_id:
#         print("No data found for 'LIPSTICK'")
#         return

#     # Append the new timestamp to the 'classify time' list
#     if "classify time" in data_of_id:
#         data_of_id["classify time"].append(new_attendance_time)
#     else:
#         data_of_id["classify time"] = [new_attendance_time]

#     # Update the database with the modified data
#     ref.child(id).update(data_of_id)




#     height, width = 256, 256
#     image = np.zeros((height, width, 3), dtype=np.uint8)

#     # Tạo màu nền xanh lá cây
#     image[:] = [0, 255, 0]  # Màu xanh lá cây

#     # Vẽ một hình tròn màu đỏ ở giữa ảnh
#     cv2.circle(image, (height//2, width//2), height//4, (255, 0, 0), -1)
import cv2
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime
import numpy as np
import io

def addAttendanceTime(id, image):
    # Reference to the 'CLASSIFY' node in your database
    ref = db.reference('CLASSIFY')

    # Generate the current time as a string
    new_attendance_time = str(datetime.now())

    # Retrieve data for the 'LIPSTICK' child node
    data_of_id = ref.child(id).get()

    if not data_of_id:
        print(f"No data found for '{id}'")
        return

    # Append the new timestamp to the 'classify time' list
    if "classify time" in data_of_id:
        data_of_id["classify time"].append(new_attendance_time)
    else:
        data_of_id["classify time"] = [new_attendance_time]

    # Update the database with the modified data
    ref.child(id).update(data_of_id)

    # Create an image using OpenCV
    

    # Determine the name for the new image file
    last_index = len(data_of_id["classify time"]) - 1
    image_name = f"{id}{last_index}.jpg"

    # Encode image as JPEG
    success, encoded_image = cv2.imencode('.jpg', image)
    if not success:
        print(f"Failed to encode image {image_name}.")
        return

    # Convert the encoded image to a byte array
    image_bytes = encoded_image.tobytes()

    # Initialize storage reference
    try:
        bucket = storage.bucket()
        blob = bucket.blob(f'Images/{image_name}')

        # Upload the image to Firebase Storage
        blob.upload_from_string(image_bytes, content_type='image/jpeg')
        print(f"Image {image_name} uploaded to Firebase Storage.")
    except Exception as e:
        print(f"Failed to upload image {image_name}. Error: {e}")


