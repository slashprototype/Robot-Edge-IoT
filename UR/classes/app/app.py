from threading import Thread
import sys
import time
from classes.app.utils.functions import search_script,send_robot_action,get_robot_targets

class App ():
    def __init__(self, mqtt,robot,subscribe_topics,publish_topics,routines_path):
        self.mqtt = mqtt
        self.robot = robot
        self.subscribe_topics = subscribe_topics
        self.publish_topics = publish_topics
        self.routines_path = routines_path
        self.running = False

        self.mqtt_ok = False
        self.robot_ok = False

        self.fsm_robot_control = 0
        self.fsm_robot_sync = 0
        self.fsm_mqtt_sync = 0

        self.mqtt_thread = Thread(target=self.mqtt_sync)
        self.mqtt_thread.setDaemon(True)
        self.robot_monitoring_thread = Thread(target=self.robot_sync)
        self.robot_monitoring_thread.setDaemon(True)
        self.robot_control_thread = Thread(target=self.robot_control)
        self.robot_control_thread.setDaemon(True)
        
        self.main_loop()

    def start_app(self):
        self.running = True
        print('Initializing App...')
        time.sleep(1)
        self.mqtt_thread.start()
        self.robot_monitoring_thread.start()    
        self.robot_control_thread.start()    
        


    def close_app(self):
        self.running = False
        raise Exception('App interruption')
        


# ---------------------THREADS AND CONTROL LOOP---------------------------

    def main_loop(self):
        self.start_app()
        while True:  
            try:
                # pass
                time.sleep(1)
                # print('mqtt_ok', self.mqtt_ok, self.mqtt.subscribe_status,self.mqtt.connection_status
                # , 'robot_ok', self.robot_ok)
                if self.mqtt_ok and self.robot_ok:
                    print('Communications are ok')
                else:
                    print('ROBOT alarms: ',self.robot.alarm, self.robot.alarm_id)
                    if self.mqtt.connection_status == False:
                        print('MQTT connection error')
                    elif self.mqtt.subscribe_status == False:
                        print('MQTT subscribe error')
                    print('\n')

            except KeyboardInterrupt:
                print('interruptions')            
                self.close_app() 
                

    def mqtt_sync(self):
        
        while (self.running):
            try:

                # FIRST INIT
                if self.fsm_mqtt_sync == 0:
                    self.fsm_mqtt_sync = 10
                
                #CONNECTING
                if self.fsm_mqtt_sync == 10:
                    self.mqtt.connect(self.subscribe_topics)
                    if self.mqtt.connection_status == True:
                        self.fsm_mqtt_sync = 20
                    else:
                        self.fsm_mqtt_sync = 10

                #RUNNING
                if self.fsm_mqtt_sync == 20:
                    try:
                        received_msg = self.mqtt.get_data()
                        self.mqtt_ok = True
                    except:
                        self.fsm_mqtt_sync = 30

                # ALARM
                if self.fsm_mqtt_sync == 30:
                    self.mqtt_ok = False
                    if self.mqtt.connection_status == False:
                        self.fsm_mqtt_sync = 10
                    
                    elif self.mqtt.subscribe_status == False:
                        self.fsm_mqtt_sync = 20

                    else:
                        print('unknow error raised')
                        self.fsm_mqtt_sync = 30

            except:
                # END WHILE LOOP    
                print('ending mqtt')
                self.mqtt_sync.join() 
                break
        
        
    

    def robot_sync(self):
        while (self.running):
            try:
                if self.fsm_robot_sync == 0:
                    self.fsm_robot_sync = 10

                if self.fsm_robot_sync == 10:
                    self.robot.connect()
                    if self.robot.connection_status == True:
                        self.fsm_robot_sync = 20
                    else:
                        self.fsm_robot_sync = 10

                if self.fsm_robot_sync == 20:
                    try:
                        self.robot.get_data()
                        self.robot_ok = True
                    except:
                        self.fsm_robot_sync = 30
                
                # ALARM
                if self.fsm_robot_sync == 30:
                    self.robot_ok = False
                    self.fsm_robot_sync = 10
                    
            except:
                # END WHILE LOOP
                print('ending robot monitoring loop')
                self.robot_sync.join()
                break

        


    def robot_control(self):
        while (self.running):
            try:
                if self.mqtt_ok and self.robot_ok:
                    
                    if self.fsm_robot_control == 1:
                        print('Initial status in robot control')
                        time.sleep(5)
                        self.fsm_robot_control = 10

                    if self.fsm_robot_control == 10:
                        print('initializing robot...')
                        time.sleep(1)
                        self.fsm_robot_control = 20

                    if self.fsm_robot_control == 20:
                        print('waiting for execute')
                        time.sleep(1)

                    if self.fsm_robot_control == 21:
                        print('start working')
                        time.sleep(1)
                    
                    # ALARM
                    if self.fsm_robot_control == 30:
                        time.sleep(1)
                        print('robot control exceptions')
                else:
                    # print('Reset machine to 0')
                    self.fsm_robot_control = 0
                
            except:
                # END WHILE LOOP
                print('ending robot control loop')          
                self.robot_control.join()
                break

        


if __name__ == '__main__':
    app = App('broker','UR3-A','subscrib','publish','path')


