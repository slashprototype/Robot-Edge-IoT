from threading import Thread
import sys
import time

class App ():
    def __init__(self, mqtt,robot,subscribe_topics,publish_topics,routines_path):
        self.mqtt = mqtt
        self.robot = robot
        self.subscribe_topics = subscribe_topics
        self.publish_topics = publish_topics
        self.routines_path = routines_path
        self.running = False
        

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
                pass
                # print('fsm_mqtt_sync', self.fsm_mqtt_sync)
                # print('fsm_robot_sync', self.fsm_robot_sync)
                # print('fsm_robot_control', self.fsm_robot_control)
                
            except KeyboardInterrupt:
                print('interruptions')            
                self.close_app() 
                

    def mqtt_sync(self):
        while (self.running):
            try:
                if self.fsm_mqtt_sync == 0:
                    print('creating mqtt client')
                    time.sleep(5)
                    self.fsm_mqtt_sync = 10

                if self.fsm_mqtt_sync == 10:
                    print('connect to broker...')
                    self.mqtt.connect(self.subscribe_topics)
                    if self.mqtt.mqtt_ok == True:
                        self.fsm_mqtt_sync = 20
                    else:
                        self.fsm_mqtt_sync = 30

                if self.fsm_mqtt_sync == 20:
                    time.sleep(0.5)
                    try:
                        received_msg = self.mqtt.get_data()
                        print(received_msg)
                    except:
                        self.fsm_mqtt_sync = 30

                # ALARM
                if self.fsm_mqtt_sync == 30:
                    print('mqtt exceptions')
                    time.sleep(0.5)
                    
                    if self.mqtt.mqtt_ok == False:
                        self.fsm_mqtt_sync = 10
                    else:
                        print('some exceptions in subscribe or publish has ocurred')

            except:
                # END WHILE LOOP    
                print('ending mqtt')
                self.mqtt_sync.join() 
                break
        
        
    

    def robot_sync(self):
        while (self.running):
            try:
                if self.fsm_robot_sync == 0:
                    print('create a robot instance')
                    time.sleep(1)
                    self.fsm_robot_sync = 10

                if self.fsm_robot_sync == 10:
                    print('connecting to robot...')
                    try:
                        self.robot.connect()
                        self.robot.get_data()
                        if self.robot.robot_ok == True:
                            self.fsm_robot_sync = 20
                    except:
                        print('Connection problem...')
                        self.fsm_robot_sync = 30

                if self.fsm_robot_sync == 20:
                    print('robot ok')
                
                # ALARM
                if self.fsm_robot_sync == 30:
                    print('robot exceptions')
            except:
                # END WHILE LOOP
                print('ending robot monitoring loop')
                self.robot_sync.join()
                break

        


    def robot_control(self):
        while (self.running):
            try:
                time.sleep(15)
        
                if self.fsm_robot_control == 10:
                    print('initializing robot...')

                if self.fsm_robot_control == 20:
                    print('waiting for execute')

                if self.fsm_robot_control == 21:
                    print('start working')
                
                # ALARM
                if self.fsm_robot_control == 30:
                    print('robot control exceptions')
            except:
                # END WHILE LOOP
                print('ending robot control loop')          
                self.robot_control.join()
                break

        


if __name__ == '__main__':
    app = App('broker','UR3-A','subscrib','publish','path')


