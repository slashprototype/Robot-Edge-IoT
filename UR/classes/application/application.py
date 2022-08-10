from ast import While
from threading import Thread
import sys
import time
from tracemalloc import stop
from unittest import runner

class Application ():
    def __init__(self, mqtt,robot,subscribe_topics,publish_topics,routines_path):
        self.mqtt = mqtt
        self.robot = robot
        self.subscribe_topics = subscribe_topics
        self.publish_topics = publish_topics
        self.routines_path = routines_path
        self.running = False
        
        self.robot_thread = Thread(target=self.robot_loop, args =(lambda : self.running, ),daemon=True)
        self.mqtt_thread = Thread(target=self.mqtt_loop)
        self.main_thread = Thread(target=self.main_loop)
        
        self.start_app()
        self.main_loop()

    def start_app(self):
        self.running = True
        self.robot_thread.start()
        self.mqtt_thread.start()


    def close_app(self):

        for i in range (5):
            self.running = False
            time.sleep(0.1)
            self.robot_thread.join()
            self.mqtt_thread.join()
        print('clossing app')
        sys.exit()


# ---------------------THREADS AND CONTROL LOOP---------------------------

    def main_loop(self):
        while True:
            try:
                pass
            except KeyboardInterrupt:            
                self.close_app()
                

    def mqtt_loop(self):
        while (self.running):
            time.sleep(0.1)
            print(self.mqtt)
    
    def robot_loop(self, stop):
        while (self.running):
            time.sleep(0.1)
            print(self.robot)


if __name__ == '__main__':
    app = Application('broker','UR3-A','subscrib','publish','path')


