from mqtt import Mqtt
import time

subscribe_topics = [
    "/PCB/CELL-A/UR3-A/TEST-1/VALUE"
]

publish_topics= [
    "/PCB/CELL-A/UR3-A/TEST-2/VALUE",
]

mqtt = Mqtt('10.40.30.50', 31285, 30,'UR3-Test_subscribe')
mqtt_ok = mqtt.connect(subscribe_topics)

while True:
    mqtt_ok, data = mqtt.get_data()
    mqtt.publish(subscribe_topics)
    print(data)
    time.sleep(1)