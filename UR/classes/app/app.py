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

        # Set initial variables to start running the app
        self.mqtt_ok = False
        self.robot_ok = False
        self.robot_sync_setup = False
        self.robot_control_setup = False
        self.exception = False
        self.control_status = 187

        # Finite state machine for robot control
        self.fsm_robot_control = 0.0
        self.fsm_robot_control_type = ''

        # Finite state machine for robot rtde syncronization
        self.fsm_robot_sync = 0
        self.fsm_robot_sync_type = ''

        # Finite state machine for mqtt broker syncronization
        self.fsm_mqtt_sync = 0
        self.fsm_mqtt_sync_type = ''
        
        # New threads for manage while loops
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
        counter_1 = 0
        old = -2
        new = -1
        time.sleep(3)
        while True:  
            try:
                time.sleep(0.01)
                
                if self.mqtt_ok and self.robot_ok:  
                    if self.ctrl_emergency_stop != 0:
                        print('Emergency stop')
                        time.sleep(1)
                        self.fsm_robot_control = 30
                    counter_1 = 0
                    #Print control finite state machine type
                    new = self.fsm_robot_control_type
                    if new != old:
                        print(new)
                        old = new
                else:
                    if self.robot_control_setup: 
                        self.fsm_robot_control = 30
                    if counter_1 >= 100:
                        print('ROBOT alarms: ',self.robot.alarm, self.robot.alarm_id)
                        print('MQTT alarm:',self.mqtt.alarm,
                              'Connection status:',self.mqtt.connection_status,
                              'subscribe status:', self.mqtt.subscribe_status)
                        counter_1 = 0
                    else:
                        counter_1 = counter_1 + 1
                
                # if self.robot_control_setup:
                #     if self.robot_status <= 6 and self.fsm_robot_control != 10 and self.fsm_robot_control != 30 :
                #         self.fsm_robot_control = 30
                #         if self.robot_status == 0:
                #             print('UNKNOW ERROR IN ROBOT STATUS ID')
                #             time.sleep(2)

            except KeyboardInterrupt:
                print('interruptions')            
                self.close_app() 


    def mqtt_sync(self):
        counter_1 = 0
        while (self.running):
            time.sleep(0.01)
            try:

                # FIRST START
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
                        topic_value = self.mqtt.get_data()
                        self.ctrl_command = topic_value['ss_command']
                        self.ctrl_execute = topic_value['ss_execute']
                        self.ctrl_emergency_stop = topic_value['ss_emergency_stop']
                        self.ctrl_speed = topic_value['ss_speed']
                        self.ctrl_visor_result = topic_value['robot_visor']
                        self.ctrl_qr_result = topic_value['ss_qr']
                        self.ctrl_inspection_2_resultwork = topic_value['inspection_2_resultwork']
                        self.ctrl_inspection_2_status = topic_value['inspection_2_status']
                        
                        if self.robot_sync_setup == True and counter_1 >= 100:
                            self.mqtt.publish(self.publish_topics['position_value'],self.robot_position)
                            self.mqtt.publish(self.publish_topics['current_value'],self.robot_current)
                            self.mqtt.publish(self.publish_topics['temperature_value'],self.robot_temperature)
                            self.mqtt.publish(self.publish_topics['tool_value'],self.robot_tool)
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
                        # print('unknow error raised')
                        pass
                        
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
                # FIRST START
                if self.fsm_robot_sync == 0:
                    self.fsm_robot_sync_type = 'Initial Conditions'
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
                        self.watchdog = 1
                        self.robot.sync_config(slider_fraction = self.ctrl_speed)
                        
                        self.runtime_state = int(robot_data.get('runtime_state'))
                        self.robot_working_status = int(robot_data.get('output_int_register_0'))
                        self.robot_position = str(robot_data.get('actual_q'))
                        self.robot_current = str(robot_data.get('actual_current')) 
                        self.robot_temperature = str(robot_data.get('joint_temperatures'))
                        if self.robot.name == 'UR3-C':
                            self.robot_tool = str(robot_data.get('output_int_register_1'))
                        
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

    #LOOP FOR ROBOT CONTROL
    def robot_control(self):
        timeout = 0
        while (self.running):
            try:

                # FIRST START
                if self.fsm_robot_control == 0:
                    self.fsm_robot_control_type = 'Initial Conditions'
                    
                    # Initial status in robot control, waiting for all connections are ok
                    if self.mqtt_ok and self.robot_ok:    
                        self.robot_control_setup = True
                        self.mqtt.publish(self.publish_topics['visor_value'],0)
                        self.mqtt.publish(self.publish_topics['status_value'],187)
                        self.mqtt.publish(self.publish_topics['resultwork_value'],0)
                        # set robot register "start" to 0 for control flow
                        self.robot.sync_program(start = 0)
                        self.fsm_robot_control = 30

                if self.fsm_robot_control == 10:
                    self.fsm_robot_control_type = 'Initial Conditions'
                    if self.robot_status <= 3:
                        self.control_status = 204
                        send_robot_action(self.robot,'stop')
                        send_robot_action(self.robot,'auto_init')
                        send_robot_action(self.robot,'auto_play')                
                        timeout = 0
                
                    if self.robot_status >3 and self.robot_status <6 and timeout == 0:
                        self.control_status = 204

                    if self.robot_status >= 6:
                        timeout = 0
                        self.control_status = 170
                        if self.ctrl_execute == 0:
                            self.fsm_robot_control = 20
                    
                    if timeout >= 150:
                        print('Timeout exceed restart routine...')
                        self.control_status = 255
                        self.fsm_robot_control = 30

                    timeout = timeout + 1
                        
                    time.sleep(0.1)
                    
                if self.fsm_robot_control == 20:
                    self.fsm_robot_control_type = 'set initial control status'
                    self.mqtt.publish(self.publish_topics['visor_value'],0)
                    self.mqtt.publish(self.publish_topics['status_value'],170)
                    
                    time.sleep(0.1)
                    self.fsm_robot_control = 20.1

                if self.fsm_robot_control == 20.1:
                    self.fsm_robot_control_type = 'Waiting for execute'

                    if self.ctrl_execute == 1:
                        try:
                            self.mqtt.publish(self.publish_topics['status_value'],221)
                            self.mqtt.publish(self.publish_topics['resultwork_value'],221)  

                            file = self.routines_path+search_script(self.robot.name,self.ctrl_command)
                            print('routine script selected: ', file)
                            target_id = 0
                            targets, targets_len = get_robot_targets(file)
                            self.fsm_robot_control = 20.2
                        except:
                            print('Error when searching file: ',file)
                            self.fsm_robot_control = 30 

                if self.fsm_robot_control == 20.2:
                    self.fsm_robot_control_type = 'Analizing script... waiting for execute = 0'
                    
                    if self.ctrl_execute == 0:
                        if self.runtime_state != 2:
                            send_robot_action(self.robot,'start')
                        else:
                            if target_id < targets_len:
                                # Get move type, tool, visor, inspection, clamp action
                                target_type = targets[target_id][5]
                                
                                # Robot Normal action (move,tool)
                                if target_type <= 6:
                                    self.fsm_robot_control = 20.3

                                # Robot Visor routines
                                elif target_type == 10 or target_type == 11:
                                    self.fsm_robot_control = 21
                                
                                # Robot Inspection routine
                                elif target_type == 12:
                                    self.fsm_robot_control = 22
                                
                                # Robot Clamp control
                                elif target_type == 15:
                                    self.fsm_robot_control = 23
                                
                                # Robot return (experimental)
                                elif target_type == 19:
                                    self.fsm_robot_control = 24

                                # Robot Axis movement
                                elif target_type>=20:
                                    self.fsm_robot_control = 24
                                
                            else:
                                print('Routine Complete succesfully')
                                self.mqtt.publish(self.publish_topics['status_value'],170)
                                self.mqtt.publish(self.publish_topics['resultwork_value'],170)
                                # time.sleep(1)
                                self.fsm_robot_control = 20
                        # time.sleep(0.1)

                if self.fsm_robot_control == 20.3:
                    self.fsm_robot_control_type = 'Send actual "target" and "start" to robot'
                    # print(self.robot_working_status)
                    if self.robot_working_status == 1:
                        print('sending target', target_id)
                        self.robot.sync_setpoint(targets,target_id)
                        self.robot.sync_program(start = 1)
                        print(targets[target_id])
                        self.fsm_robot_control = 20.4
                    time.sleep(0.1)

                if self.fsm_robot_control == 20.4:
                    self.fsm_robot_control_type = 'Waiting for finish movement'
                    if self.robot_working_status == 3:
                        self.robot.sync_program(start = 0)
                        target_id = target_id + 1
                        self.fsm_robot_control = 20.2
                    time.sleep(0.1)
                
                if self.fsm_robot_control == 21:
                    self.fsm_robot_control_type = 'Visor routine selected, sending trigger...'
                    # Send trigger to vision sensor
                    self.mqtt.publish(self.publish_topics['visor_value'],2)
                    self.fsm_robot_control = 21.1
                
                if self.fsm_robot_control == 21.1:
                    # Waiting for visor detect result value
                    if target_type == 10:
                        if self.ctrl_visor_result == 170:
                            self.fsm_robot_control = 21.2
                        print('visor result = ',self.ctrl_visor_result) 
                    
                    # Waiting for visor code qr result
                    if target_type == 11:
                        if self.ctrl_visor_result == 170 and self.ctrl_qr_result == 170:
                            self.fsm_robot_control = 21.2
                        print('visor result = ',self.ctrl_visor_result, 'qr result=',self.ctrl_qr_result)
                    time.sleep(0.5)
                
                if self.fsm_robot_control == 21.2:
                    self.mqtt.publish(self.publish_topics['visor_value'],0)
                    target_id = target_id + 1
                    self.fsm_robot_control = 20.2

                if self.fsm_robot_control == 22:
                    self.fsm_robot_control_type = 'Camera inspection routine'
                    if self.ctrl_inspection_2_status == 170:
                        self.mqtt.publish(self.publish_topics['inspection_2_command_value'],100)
                        time.sleep(0.1)
                        self.mqtt.publish(self.publish_topics['inspection_2_execute_value'],1)
                        self.fsm_robot_control = 22.1
                    else:
                        print('Camera is not ready..status is: ',self.ctrl_inspection_2_status) 
                        time.sleep(0.5)
                
                if self.fsm_robot_control == 22.1:
                    self.fsm_robot_control_type = 'Waiting for camera response...'
                    if self.ctrl_inspection_2_resultwork == 221:
                        self.mqtt.publish(self.publish_topics['inspection_2_execute_value'],0)
                        self.fsm_robot_control = 22.2

                if self.fsm_robot_control == 22.2:
                    self.fsm_robot_control_type = 'Waiting for inspection finished...'
                    if self.ctrl_inspection_2_resultwork == 187:
                        print('Inspection finished correctly')
                        target_id = target_id + 1
                        self.fsm_robot_control = 20.2
                    
                # ALARM
                if self.fsm_robot_control == 30:
                    self.fsm_robot_control_type = 'Alarm status'
                    flag = 0
                    if self.mqtt_ok == True:
                        self.control_status = 255
                        # self.mqtt.publish(self.publish_topics['visor_value'],255)
                        self.mqtt.publish(self.publish_topics['status_value'],255)
                        # self.mqtt.publish(self.publish_topics['resultwork_value'],255)
                    
                    if self.robot_ok == True:
                        self.robot.sync_program(start = 0)
                        # self.robot.sync_config(slider_mask = 1, slider_fraction = 0)
                        if self.runtime_state != 1:
                            print(self.runtime_state)
                            send_robot_action(self.robot,'stop')
                        
                    if self.ctrl_command == 10 and self.ctrl_execute == 1:
                        # self.mqtt.publish(self.publish_topics['visor_value'],187)
                        self.fsm_robot_control = 10                
                    time.sleep(1)
                    
            except:
                # END WHILE LOOP
                print('ending robot control loop')          
                self.robot_control.join()
                break


