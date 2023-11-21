import mysql.connector
import base64
import numpy as np
import cv2
from ultralytics import YOLO

model = YOLO("best.pt")
# image_path = "/home/centos/prj/static/진라면컵.jpg"
image_path = "/home/centos/prj/images/DB_image.jpg"
img = cv2.imread(image_path)
results = model([image_path])

desired_classes = ["shirmp"]

for result in results:
    boxes = result.boxes.xyxy.numpy()
    classes = result.boxes.cls.numpy()
    confidences = result.boxes.conf.numpy()
    orig_shape_x = np.array(result.boxes.orig_shape)[0]
    orig_shape_y = np.array(result.boxes.orig_shape)[1]

BOX_RESIZE_FACTOR = 0.6

for box, class_id in zip(boxes, classes):
        class_name = model.names[int(class_id)]
        if class_name in desired_classes:
            y1, x1, y2, x2 = map(int, box[:4])

            # Compute new bounding box coordinates
            new_x1 = int(x1 + (x2 - x1) * (1 - BOX_RESIZE_FACTOR) / 2)
            new_x2 = int(x2 - (x2 - x1) * (1 - BOX_RESIZE_FACTOR) / 2)
            new_y1 = int(y1 + (y2 - y1) * (1 - BOX_RESIZE_FACTOR) / 2)
            new_y2 = int(y2 - (y2 - y1) * (1 - BOX_RESIZE_FACTOR) / 2)

            cv2.rectangle(img, (new_y1, new_x1), (new_y2, new_x2), (0, 255, 0), 15)
cv2.imwrite('/home/centos/prj/output_img/output.jpg', img)
