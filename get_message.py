import paho.mqtt.client as mqtt
import base64
import cv2
import numpy as np
import mysql.connector

# MQTT 클라이언트 설정
client = mqtt.Client("sub1")


# MQTT 브로커에 연결
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", str(rc))
    client.subscribe("mqtt_image_topic")  # 이미지 토픽 구독


# 이미지 수신 및 처리
def on_message(client, userdata, msg):
    if msg.topic == "mqtt_image_topic":
        save_to_database(msg.payload)


# 데이터베이스 저장
def save_to_database(compressed_image):
    # 데이터베이스 연결 및 데이터 저장 코드
    connection = mysql.connector.connect(
        host="3.36.232.50", user="centos", password="Aisl1234!", database="Finder_db"
    )

    cursor = connection.cursor()
    sql = "UPDATE camera SET camera1= %s WHERE idcamera=1"
    cursor.execute(sql, (compressed_image,))
    connection.commit()

    cursor.close()
    connection.close()


client.on_connect = on_connect
client.on_message = on_message

client.connect("3.36.232.50", 1883, 120)
client.loop_forever()
