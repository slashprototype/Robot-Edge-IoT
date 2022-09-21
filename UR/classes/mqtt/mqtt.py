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
        self.topic_value = {}
        self.topic_value_len = 8
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
            for key,value in subscribe_topics.items():
                client.subscribe(value)

        def on_disconnect(client, userdata, rc):
            self.connection_status = False
            print('CLIENT DISCONNECTED!!!!')
        
        def on_message(client, userdata, msg):
            # COMMAND
            try:

                if msg.topic == subscribe_topics['ss_command']:
                    self.topic_value['ss_command'] = int(msg.payload.decode('UTF-8'))
                # EXECUTE
                if msg.topic == subscribe_topics['ss_execute']:
                    self.topic_value['ss_execute'] = int(msg.payload.decode('UTF-8'))
                # EMERGENCY STOP
                if msg.topic == subscribe_topics['ss_emergency_stop']:
                    self.topic_value['ss_emergency_stop'] = int(msg.payload.decode('UTF-8'))
                # SPEED
                if msg.topic == subscribe_topics['ss_speed']:
                    self.topic_value['ss_speed'] = float(msg.payload.decode('UTF-8'))

                # if msg.topic == subscribe_topics['ss_tool']:
                #     self.topic_value['ss_tool'] = int(msg.payload.decode('UTF-8'))      
                #VISOR VALUE
                if msg.topic == subscribe_topics['robot_visor']:
                    self.topic_value['robot_visor'] = int(msg.payload.decode('UTF-8'))
                    
                if msg.topic == subscribe_topics['ss_qr']:
                    self.topic_value['ss_qr'] = int(msg.payload.decode('UTF-8'))

                if msg.topic == subscribe_topics['operation_mode']:
                    self.topic_value['operation_mode'] = str(msg.payload.decode('UTF-8'))
                
                if msg.topic == subscribe_topics['inspection_2_resultwork']:
                    self.topic_value['inspection_2_resultwork'] = int(msg.payload.decode('UTF-8'))

                if msg.topic == subscribe_topics['inspection_2_status']:
                    self.topic_value['inspection_2_status'] = int(msg.payload.decode('UTF-8'))
                
                
                self.receive_status = True
            except:
                print('some problem in subscribe topics')
                self.receive_status = False
        
        if self.setup == False:
            for key,value in subscribe_topics.items():
                self.topic_value[key]=0

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

        # Check connection before send data
        if self.connection_status == True and self.receive_status == True:    
            self.subscribe_status = True
            return (self.topic_value)

        else:            
            self.subscribe_status = False
            if self.connection_status == False:
                self.alarm = 'Connection error ocurred when getting data'
                raise Exception('Connection error ocurred when getting data')
            else:
                self.alarm = 'A topic data is missing, just received: ',len(self.topic_value),' topics info'
                raise Exception('A topic data is missing, just received: ',len(self.topic_value),' topics info')
            



