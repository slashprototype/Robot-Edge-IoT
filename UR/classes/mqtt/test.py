from mqtt import Mqtt
import time

subscribe_topics = [
        "/PCB/CELL-A/UR3-A/CONTROLLER/COMMAND/TIMESTAMP",
        "/PCB/CELL-A/UR3-A/CONTROLLER/COMMAND/VALUE",
        "/PCB/CELL-A/UR3-A/CONTROLLER/EXECUTE/TIMESTAMP",
        "/PCB/CELL-A/UR3-A/CONTROLLER/EXECUTE/VALUE",
        "/PCB/CELL-A/UR3-A/CONTROLLER/EMERGENCYSTOP/TIMESTAMP",
        "/PCB/CELL-A/UR3-A/CONTROLLER/EMERGENCYSTOP/VALUE",
        "/PCB/CELL-A/UR3-A/CONTROLLER/SPEED/VALUE",
        "/PCB/CELL-A/UR3-A/MONITORING/TOOL/VALUE"
    ]

mqtt = Mqtt('10.40.30.50', 31285, 30,'UR3-Test')
mqtt_ok = mqtt.connect(subscribe_topics)
while True:
    mqtt_ok, data = mqtt.get_data()
    print(data)
    time.sleep(1)