import paho.mqtt.client as mqtt
import ssl



class Mqtt():

    def __init__(self, ip, port, keep_alive,client_name):    
        self.ip = ip
        self.port = port
        self.keep_alive = keep_alive
        self.client_name = client_name
        self.keyPaths = "classes/mqtt/authFiles/"
        self.received_msg = {}
        self.mqtt_ok = False
        self.client = mqtt.Client(client_id=self.client_name,
                        clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

    def connect(self,subscribe_topics):
            # Subscribe to MQTT broker topics
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code", rc)
            # Subscribe to REGOUT
            for i in subscribe_topics:
                client.subscribe(i)
        
        def on_message(client, userdata, msg):
            
            try:
                # COMMAND
                if msg.topic == subscribe_topics[1]:    
                    self.received_msg['command'] = int(msg.payload.decode('UTF-8'))
                # EXECUTE
                if msg.topic == subscribe_topics[3]:
                    self.received_msg['execute'] = int(msg.payload.decode('UTF-8'))
                # EMERGENCY STOP
                # if msg.topic == subscribe_topics[5]:
                    # self.received_msg['emergency_stop'] = int(msg.payload.decode('UTF-8'))
                # SPEED
                if msg.topic == subscribe_topics[6]:
                    self.received_msg['speed'] = float(msg.payload.decode('UTF-8'))
                #VISOR VALUE
                if msg.topic == subscribe_topics[8]:
                    self.received_msg['visor_result'] = int(msg.payload.decode('UTF-8'))
                    
                if msg.topic == subscribe_topics[9]:
                    self.received_msg['qr_result'] = int(msg.payload.decode('UTF-8'))
                
                if msg.topic == subscribe_topics[7]:
                    self.received_msg['tool_status'] = int(msg.payload.decode('UTF-8'))

            except:
                pass
            
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.username_pw_set(username="user01", password="user01")
        self.client.tls_set(ca_certs=self.keyPaths+"ca.crt", certfile=self.keyPaths+"client01.crt",
                            keyfile=self.keyPaths+"client01.key", cert_reqs=ssl.CERT_NONE,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.client.tls_insecure_set(True)

        print("Connecting to broker...")
        try:
            self.client.connect(self.ip,self.port,self.keep_alive)
            print('Connected succesfully to broker')
            self.client.loop_start()
            self.mqtt_ok = True
        except:
            print('cannot start connection with broker')
            self.mqtt_ok = False

    def publish(self,publish_topic,value):
        
        try:      
            self.client.publish(publish_topic,value,1,True)
            self.mqtt_ok = True
        except:
            print('Error in robot publish')
            self.mqtt_ok = False

    def get_data(self):

        if len(self.received_msg) >= 4:
            # print(received_msg)
            self.mqtt_ok = True
            return (self.received_msg)

        else:
            print('A topic data is missing, just received: ',len(self.received_msg),' topics info')
            self.mqtt_ok = False
            return (self.received_msg)
            



