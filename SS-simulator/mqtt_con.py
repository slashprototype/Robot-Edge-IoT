import paho.mqtt.client as mqtt
import ssl

keyPaths = "authFiles/"
global received_msg
received_msg = ''
client = mqtt.Client(client_id="UR3e_MASTER_APP",
                    clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
                    
def mqtt_start(ip,port,keep_alive,publish_topics, subscribe_topics):
        # Subscribe to MQTT broker topics
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code", rc)
        # Subscribe to REGOUT
        for i in subscribe_topics:
            client.subscribe(i)

    
    def on_message(client, userdata, msg):
        print("Received from: ", msg.topic, msg.payload.decode('UTF-8'))
        # Data manipulation to get a list
        # received_msg = str(msg.payload).split('|')
        global received_msg
        received_msg = msg.payload.decode('UTF-8')
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username="user02", password="C1d3siMQTTUser20220322")
    client.tls_set(ca_certs=keyPaths+"ca.crt", certfile=keyPaths+"client01.crt",
                        keyfile=keyPaths+"client01.key", cert_reqs=ssl.CERT_NONE,
                        tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    client.tls_insecure_set(True)

    print("Connecting to broker...")
    try:
        client.connect(ip,port,keep_alive)
        print('Connected succesfully to broker')
        client.loop_start()
    except:
        print('cannot start connection with broker')
    




