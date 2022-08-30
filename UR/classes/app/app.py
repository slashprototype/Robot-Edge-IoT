from threading import Thread
import sys
import time
from classes.app.utils.functions import search_script,send_robot_action,get_robot_targets, get_fsm_status_type

class App ():
    def __init__(self, mqtt,robot,subscribe_topics,publish_topics,routines_path):
        self.mqtt = mqtt
        self.robot = robot
        self.subscribe_topics = subscribe_topics
        self.publish_topics = publish_topics
        self.routines_path = routines_path
        self.running = False
        self.bit_reset = True

        self.mqtt_ok = False
        self.robot_ok = False
        self.robot_sync_setup = False
        self.robot_control_setup = False
        self.exception = False

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
    
    def publish_mqtt(self, **args):
        for key,value in args.items():
            if key == 'robot_status':
                self.mqtt.publish(self.publish_topics[2],value)
            if key == 'tool':
                self.mqtt.publish(self.publish_topics[10],value)
            if key == 'execute':
                self.mqtt.publish(self.publish_topics[12],value)
            if key == 'robot_resultwork':
                self.mqtt.publish(self.publish_topics[14],value)


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
        counter_1 = 0
        old = -2
        new = -1
        while True:  
            try:
                time.sleep(0.01)
                if self.mqtt_ok and self.robot_ok:       
                    counter_1 = 0
                    new = get_fsm_status_type(self.fsm_robot_control)
                    if new != old:
                        print(new)
                        old = new
                    
                else:
                    if self.robot_control_setup: 
                        self.fsm_robot_control = 30
                    if counter_1 >= 100:
                        print('ROBOT alarms: ',self.robot.alarm, self.robot.alarm_id)
                        if self.mqtt.connection_status == False:
                            print('MQTT connection error')
                        elif self.mqtt.subscribe_status == False:
                            print('MQTT subscribe error')
                        counter_1 = 0
                    else:
                        counter_1 = counter_1 + 1

                

            except KeyboardInterrupt:
                print('interruptions')            
                self.close_app() 


    def mqtt_sync(self):
        counter_1 = 0
        while (self.running):
            time.sleep(0.01)
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
                        self.ctrl_command = received_msg['command']
                        self.ctrl_execute = received_msg['execute']
                        self.ctrl_emergency_stop = received_msg['emergency_stop']
                        self.ctrl_speed = received_msg['speed']
                        self.ctrl_visor_result = received_msg['visor_result']
                        self.ctrl_qr_result = received_msg['qr_result']
                        self.ctrl_tool_status = received_msg['tool_status']
                        
                        if self.robot_sync_setup == True and counter_1 >= 100:
                            self.mqtt.publish(self.publish_topics[4],self.robot_position)
                            self.mqtt.publish(self.publish_topics[6],self.robot_current)
                            self.mqtt.publish(self.publish_topics[8],self.robot_temperature)
                            # self.mqtt.publish(self.publish_topics[10],self.robot_tool)
                            counter_1 = 0
                        
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
                counter_1 = counter_1 + 1
            except:
                # END WHILE LOOP    
                print('ending mqtt')
                self.mqtt_sync.join() 
                break
        
        
    

    def robot_sync(self):
        while (self.running):
            time.sleep(0.01)
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
                        robot_data,robot_status = self.robot.get_data()
                        self.robot_status = robot_status
                        self.robot.sync_config(slider = 1, watchdog = 0)
                        self.robot.sync_config(slider_fraction = self.ctrl_speed)
                        
                        self.robot_working_status = int(robot_data.get('output_int_register_0'))
                        self.robot_position = str(robot_data.get('actual_q'))
                        self.robot_current = str(robot_data.get('actual_current')) 
                        self.robot_temperature = str(robot_data.get('joint_temperatures'))
                        # self.robot_tool = str(robot_data.get('output_int_register_1'))
                        
                        self.robot_sync_setup = True
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
                if self.fsm_robot_control == 0:
                    # Initial status in robot control
                    if self.mqtt_ok and self.robot_ok:
                        self.robot_control_setup = True
                        self.robot_tool = 0
                        self.mqtt.publish(self.publish_topics[10],self.robot_tool)
                        self.robot.sync_program(start = 0)
                        
                        self.fsm_robot_control = 30

                        

                if self.fsm_robot_control == 10:
                    send_robot_action(self.robot,'stop')
                    send_robot_action(self.robot,'auto_init')
                    send_robot_action(self.robot,'auto_play')
                    if self.robot_status >= 6:
                        self.publish_mqtt(robot_resultwork = 170)
                        self.fsm_robot_control = 20
                        
                    else:
                        send_robot_action(self.robot,'auto_init')
                        send_robot_action(self.robot,'auto_play')
                        print('Robot status: ',self.robot_status)
                    time.sleep(0.1)
                    

                if self.fsm_robot_control == 20:
                    time.sleep(0.1)
                    self.fsm_robot_control = 21

                if self.fsm_robot_control == 21:
                    if self.ctrl_execute == 1:
                        self.publish_mqtt(robot_resultwork = 221)
                        self.publish_mqtt(execute = 0)
                        
                        file = self.routines_path+search_script(self.robot.name,self.ctrl_command)
                        print('routine script selected: ', file)
                        target_id = 0
                        targets, targets_len = get_robot_targets(file)
                        self.fsm_robot_control = 22
                        
                        move_type = 0
                    time.sleep(0.1)     


                if self.fsm_robot_control == 22:
                    flag = 0
                    send_robot_action(self.robot,'start')
                    if target_id < targets_len:
                    
                        target_type = targets[target_id][5]

                        if target_type > 2 and target_type < 10:
                            self.fsm_robot_control = 23
                        else:
                            self.fsm_robot_control = 40
                            
                    else:
                        self.publish_mqtt(robot_resultwork = 170)
                        print('Routine Complete succesfully')
                        self.fsm_robot_control = 21
                    time.sleep(0.1)


                if self.fsm_robot_control == 23:
                    print(self.robot_working_status)
                    if self.robot_working_status == 1:
                        print('sending target', target_id)
                        self.robot.sync_setpoint(targets,target_id)
                        self.robot.sync_program(start = 1)
                        print(targets[target_id])
                        self.fsm_robot_control = 24
                    time.sleep(0.1)

                if self.fsm_robot_control == 24:
                    if self.robot_working_status == 3:
                        self.robot.sync_program(start = 0)
                        target_id = target_id + 1
                        self.fsm_robot_control = 22
                    time.sleep(0.1)

                if self.fsm_robot_control == 40:

                    if target_type == 1:
                        self.robot_tool = 170
                        self.mqtt.publish(self.publish_topics[10],self.robot_tool)
                        print('waiting for',self.ctrl_tool_status,'==', self.robot_tool)
                        if self.ctrl_tool_status == self.robot_tool:
                            target_id = target_id + 1
                            self.fsm_robot_control = 22
                            fsm_40 = 0

                    if target_type == 2:
                        self.robot_tool = 187
                        self.mqtt.publish(self.publish_topics[10],self.robot_tool)
                        print('waiting for',self.ctrl_tool_status,'==', self.robot_tool)
                        if self.ctrl_tool_status == self.robot_tool:
                            target_id = target_id + 1
                            self.fsm_robot_control = 22
                            fsm_40 = 0

                    if target_type == 10:
                        if flag == 0:
                            print('Visor detect routine')
                            self.mqtt.publish(self.publish_topics[17],2)
                            flag = 1
                        if self.ctrl_visor_result == 170:
                            target_id = target_id + 1
                            self.fsm_robot_control = 22
                            flag = 0
                        time.sleep(0.5)
                        print('visor result = ',self.ctrl_visor_result) 

                    if target_type == 11:
                        if flag == 0:
                            print('Visor code routine')
                            self.mqtt.publish(self.publish_topics[17],2)
                            flag = 1
                        if self.ctrl_visor_result == 170 and self.ctrl_qr_result == 170:
                            target_id = target_id + 1
                            self.fsm_robot_control = 22
                            flag = 0
                        time.sleep(0.5)
                        print('visor result = ',self.ctrl_visor_result, 'qr result=',self.ctrl_qr_result)

                    time.sleep(0.5)
                    
                # ALARM
                if self.fsm_robot_control == 30:
                    flag = 0
                    self.robot.sync_config(slider_mask = 1, slider_fraction = 0)
                    send_robot_action(self.robot,'stop')
                    if self.ctrl_command == 10 and self.ctrl_execute == 1:
                        self.publish_mqtt(execute = 0)
                        self.fsm_robot_control = 10                
                        time.sleep(0.1)
            except:
                # END WHILE LOOP
                print('ending robot control loop')          
                self.robot_control.join()
                break

        


if __name__ == '__main__':
    app = App('broker','UR3-A','subscrib','publish','path')


