import paho.mqtt.client as mqtt
import ssl
import time



class Mqtt():

    def __init__(self, ip, port, keep_alive,client_name):    
        self.ip = ip
        self.port = port
        self.keep_alive = keep_alive
        self.client_name = client_name
        self.keyPaths = "classes/mqtt/authFiles/"
        self.received_msg = {}
        self.received_msg_len = 7
        self.connection_status = False
        self.subscribe_status = True
        self.receive_status = False
        self.publish_status = True
        self.setup = False
        self.alarm = 'Not connected'
        self.client = mqtt.Client(client_id=self.client_name,
                        clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

    def connect(self,subscribe_topics):
            # Subscribe to MQTT broker topics
        def on_connect(client, userdata, flags, rc):
            
            print("Connected with result code", rc)
            if rc == 0:
                self.connection_status = True
            else: 
                self.connection_status = False
                
            # Subscribe to REGOUT
            for i in subscribe_topics:
                client.subscribe(i)

        def on_disconnect(client, userdata, rc):
            self.connection_status = False
            print('CLIENTE DESCONECTADO!!!!')
        
        def on_message(client, userdata, msg):
            # COMMAND
            try:
                if msg.topic == subscribe_topics[1]:    
                    self.received_msg['command'] = int(msg.payload.decode('UTF-8'))
                # EXECUTE
                if msg.topic == subscribe_topics[3]:
                    self.received_msg['execute'] = int(msg.payload.decode('UTF-8'))
                # EMERGENCY STOP
                if msg.topic == subscribe_topics[5]:
                    self.received_msg['emergency_stop'] = int(msg.payload.decode('UTF-8'))
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
                
                self.receive_status = True
            except:
                self.receive_status = False
        
        if self.setup == False:
            self.client.on_connect = on_connect
            self.client.on_disconnect = on_disconnect
            self.client.on_message = on_message
            self.client.username_pw_set(username="user01", password="user01")
            self.client.tls_set(ca_certs=self.keyPaths+"ca.crt", certfile=self.keyPaths+"client01.crt",
                                keyfile=self.keyPaths+"client01.key", cert_reqs=ssl.CERT_NONE,
                                tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
            self.client.tls_insecure_set(True)
            self.setup = True
        print('trying connection to broker...')
        try:
            self.client.connect(self.ip,self.port,self.keep_alive)
            print('connected succesfully to broker at', self.ip)
            self.connection_status = True
            self.client.loop_start()
        except:
            print('Connection failed!')
            self.connection_status = False

    def publish(self,publish_topic,value):

        try:      
            self.client.publish(publish_topic,value,1,True)
            self.publish_status = True
        except:
            print('publish problem')
            self.publish_status = False

    def get_data(self):

        if len(self.received_msg) == self.received_msg_len and self.connection_status == True and self.receive_status == True:
            self.subscribe_status = True
            return (self.received_msg)

        else:            
            self.subscribe_status = False
            if self.connection_status == False:
                self.alarm = 'Connection error ocurred when getting data'
                raise Exception('Connection error ocurred when getting data')
            else:
                self.alarm = 'A topic data is missing, just received: ',len(self.received_msg),' topics info'
                raise Exception('A topic data is missing, just received: ',len(self.received_msg),' topics info')
            



