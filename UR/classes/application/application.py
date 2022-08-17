from threading import Thread
import sys
import time

class Application ():
    def __init__(self, mqtt,robot,subscribe_topics,publish_topics,routines_path):
        self.mqtt = mqtt
        self.robot = robot
        self.subscribe_topics = subscribe_topics
        self.publish_topics = publish_topics
        self.routines_path = routines_path
        self.running = False

        self.gemma = 'D1'
        self.gemma_type = self.get_gemma_type(self.gemma)

        self.fsm_robot_control = 0
        self.fsm_robot_monitoring = 0
        self.fsm_mqtt = 0

        self.mqtt_thread = Thread(target=self.mqtt_loop)
        self.mqtt_thread.setDaemon(True)
        self.robot_monitoring_thread = Thread(target=self.robot_monitoring_loop)
        self.robot_monitoring_thread.setDaemon(True)
        self.robot_control_thread = Thread(target=self.robot_control_loop)
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
        self.robot_control_thread.join()
        self.robot_monitoring_thread.join()
        self.mqtt_thread.join()   
        sys.exit()


# ---------------------THREADS AND CONTROL LOOP---------------------------

    def main_loop(self):
        self.start_app()
        while True:
            try:
                pass
            except KeyboardInterrupt:
                print('interruptions')            
                self.close_app() 
                

    def mqtt_loop(self):
        while (self.running):
            time.sleep(0.5)
            if self.fsm_mqtt == 0:
                print('creating mqtt client')
            if self.fsm_mqtt == 10:
                print('connect to broker...')
            if self.fsm_mqtt == 20:
                print('mqtt ok')
            
            # ALARM
            if self.fsm_mqtt == 30:
                print('mqtt exceptions')

            print(self.mqtt)
        
        # END WHILE LOOP    
        print('ending mqtt')
    

    def robot_monitoring_loop(self):
        while (self.running):
            time.sleep(0.5)
            if self.fsm_robot_monitoring == 0:
                print('create a robot instance')
            if self.fsm_robot_monitoring == 10:
                print('connect to robot...')
            if self.fsm_robot_monitoring == 20:
                print('robot ok')
            
            # ALARM
            if self.fsm_robot_monitoring == 30:
                print('robot exceptions')

        # END WHILE LOOP
        print('ending robot monitoring loop')


    def robot_control_loop(self):
        while (self.running):
            time.sleep(0.5)
    
            if self.fsm_robot_control == 10:
                print('initializing robot...')

            if self.fsm_robot_control == 20:
                print('waiting for execute')

            if self.fsm_robot_control == 21:
                print('start working')
            
            # MODO
            if self.fsm_robot_control == 30:
                print('robot control exceptions')

        # END WHILE LOOP
        print('ending robot control loop')       


if __name__ == '__main__':
    app = Application('broker','UR3-A','subscrib','publish','path')


