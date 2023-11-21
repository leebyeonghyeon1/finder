import paho.mqtt.client as mqtt
import mysql.connector

# MQTT 클라이언트 설정
client = mqtt.Client("sub1")

# 데이터베이스 연결 설정
db_config = {
    'host': '3.36.232.50',
    'user': 'centos',
    'password': 'Aisl1234!',
    'database': 'Info_Sys_Project'
}

# MQTT 브로커에 연결
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", str(rc))
    client.subscribe("P")  # 이 토픽 구독

# 메시지 수신 및 처리
def on_message(client, userdata, msg):
    if msg.topic == "P":
        data = msg.payload.decode()
        temp, air_mois, phto, soil_mois = map(float, data.split(','))
        save_to_database(temp, air_mois, phto, soil_mois)

# 데이터베이스 저장
def save_to_database(temp, air_mois, phto, soil_mois):
    # 데이터베이스 연결 및 데이터 저장 코드
    connection = mysql.connector.connect(**db_config)

    cursor = connection.cursor()
    sql = "INSERT INTO smartfarm (temp, air_mois, phto, soil_mois) VALUES (%s, %s, %s, %s)"
    values = (temp, air_mois, phto, soil_mois)
    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()


client.on_connect = on_connect
client.on_message = on_message

client.connect("3.36.232.50", 1883, 60)
client.loop_forever()
