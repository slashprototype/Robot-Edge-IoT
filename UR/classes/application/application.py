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
        
        self.robot_thread = Thread(target=self.robot_loop)
        self.mqtt_thread = Thread(target=self.mqtt_loop)
        self.main_thread = Thread(target=self.main_loop)
        
        self.start_app()

    def start_app(self):
        self.running = True
        self.robot_thread.start()

    def close_app(self):
        self.running = False
        pass

    def main_loop(self):
        pass

    def mqtt_loop(self):
        pass
    
    def robot_loop(self):
        while (True):
            try:
                time.sleep(1)
                print(self.mqtt,self.robot,self.subscribe_topics,self.publish_topics,self.routines_path)
                if KeyboardInterrupt == True:
                    self.robot_thread.join(timeout=2)
                    sys.exit()
                    break
                    self.running = False
                    self.robot_thread.join()
                    
            except KeyboardInterrupt:
                self.robot_thread.join(timeout=2)
                sys.exit()
                break
                self.running = False
                self.robot_thread.join()
                sys.exit()

if __name__ == '__main__':
    app = Application('broker','UR3-A','subscrib','publish','path')


