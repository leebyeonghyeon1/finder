import mysql.connector
import base64
import numpy as np
import cv2
from ultralytics import YOLO

def  start_AI(query): 
# MySQL 연결 설정
    db_config = {
        'host': '3.36.232.50',
        'user': 'centos',
        'password': 'Aisl1234!',
        'database': 'Finder_db'
    }

    # MySQL에 연결
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # 이미지 데이터 가져오기
            query = "SELECT camera1 FROM camera WHERE idcamera = %s"  
            Image_1 = 1  
            cursor.execute(query, (Image_1,))
            image_data = cursor.fetchone()[0]

            # base64 디코딩
            image_bytes = base64.b64decode(image_data)

            # 이미지를 NumPy 배열로 변환
            nparr = np.frombuffer(image_bytes, np.uint8)

            # OpenCV로 이미지 로드
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # 이미지를 저장하거나 다른 작업 수행
            cv2.imwrite('/home/centos/prj/images/DB_image.jpg', image)  
            # AI_model(query)
            
    except Exception as e:
        print("Error:", str(e))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def AI_model(query):
    model = YOLO("3000love.pt")

    image_path = "/home/centos/prj/images/DB_image.jpg"
    img = cv2.imread(image_path)
    results = model([image_path])

    desired_classes = [query]

    for result in results:
        boxes = result.boxes.xyxy.numpy()
        classes = result.boxes.cls.numpy()
        confidences = result.boxes.conf.numpy()
        orig_shape_x = np.array(result.boxes.orig_shape)[0]
        orig_shape_y = np.array(result.boxes.orig_shape)[1]

        for box, class_id in zip(boxes, classes):
            class_name = model.names[int(class_id)]
            if class_name in desired_classes:
                y1, x1, y2, x2 = map(int, box[:4])
                x1 = orig_shape_x - x1
                x2 = orig_shape_x - x2
                print(y1, x1, y2, x2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 15)
                # cv2.putText(img, class_name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) # 텍스트 출력 관련 문장


    cv2.imwrite('/home/centos/prj/output_img/output.jpg', img)