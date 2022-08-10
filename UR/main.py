from distutils.util import execute
import time
from turtle import position
import utils.text_processor as text_processor
from datetime import datetime
import sys

datetime.now().isoformat()

#-----------------------USEFULL FUNCTIONS ----------------------------------------------------------------------#   

def send_robot_action(robot, action):
    running = True
    i = 0
    print('sending', action, 'to robot',robot.name)
    try:
        while running:
            robot.sync_config(watchdog = 0)
            robot.get_data()
            time.sleep(0.1)
            if i == 0:
                robot.sync_control(action,1)
            if i == 5:
                robot.sync_control(action,0)
            if i == 10:
                running = False
            else:
                i = i + 1
    except KeyboardInterrupt:
        robot.disconnect()
        sys.exit()

def search_script(robot_name,command):
        type_receipt = {'1':'MOVE','2':'PICK','3':'PLACE','4':'SNAP'}
        str_command = str(command)
        file = ''
        if len(str_command) == 3:
            station =   str_command[0] 
            type = str_command[1]
            zone_ID = str_command[2]
            robot_name_ID = robot_name[len(robot_name)-1]
        file = 'R'+robot_name_ID+'_E'+station+'_'+type_receipt[type]+'_'+str_command+'.script'
        return (file)

def get_robot_targets(file):
    targets = text_processor.process(file)
    targets_len = len(targets)
    return (targets,targets_len)



#-----------------------ROBOT LOOP ----------------------------------------------------------------------#

# Thread Loop
def control_loop(mqtt,robot,subscribe_topics,publish_topics,routines_path):

    file = ''
    old = 1
    new = 0
    target_id = 0
    stm_com = 0
    robot_status = 0

    try:
        while(True):
            time.sleep(0.05)
            
            # INITALIZE BROKER COMMUNICATION AND GET DATA
            # MQTT OK
            if mqtt.mqtt_ok:
                received_msg = mqtt.get_data()
                # GET TOPICS VARIABLE
                ctrl_commad = received_msg['command']
                ctrl_execute = received_msg['execute']
                ctrl_emergency_stop = received_msg['emergency_stop']
                ctrl_speed = received_msg['speed']
                
                
                # ROBOT OK
                if robot.robot_ok:
                    # GET ROBOT DATA
                    try:
                        robot_data,robot_status = robot.get_data()
                        robot.sync_config(slider = 1, watchdog = 0)
                        status = robot_data.get('output_int_register_0') 
                        runtime_state = robot_data.get('runtime_state') 
                        # print(robot_status)
                    except:
                        print('An error has ocurred while getting data from robot')
                        robot_status = 0

                    if robot_status >= 6:
                        #SYNCRONIZE BROKER CONFIGURATION VARIABLES TO ROBOT 
                        robot.sync_config(slider_fraction = ctrl_speed) 

                        # ROUTINE SCRIPT SELECTION
                        new = ctrl_commad
                        if (new != old) and (ctrl_commad != 0):
                            old = ctrl_commad
                            print('new command received!')

                            try:
                                if stm_com != 0:
                                    send_robot_action(robot,'stop')
                                file = routines_path+search_script(robot.name,ctrl_commad)
                                print('routine script selected: ', file)
                                target_id = 0
                                targets, targets_len = get_robot_targets(file)
                                robot.sync_program(start = 0)
                                robot.sync_setpoint(targets,target_id)
                                
                                robot_data,robot_status = robot.get_data()
                                runtime_state = robot_data.get('runtime_state') 

                                #ROBOT IS IN "PLAY" MODE
                                if stm_com != 0 or runtime_state != 2:
                                    send_robot_action(robot,'start')
                                    robot_data,robot_status = robot.get_data()
                                    runtime_state = robot_data.get('runtime_state') 
                                    if runtime_state == 2:
                                        stm_com = 1
                                    # else:
                                    #     robot_status = 5
                                    #     print('Robot Cannot start working, remote is not active')
                                else:
                                    stm_com = 1

                            except:
                                print('Routine file problem, stopping robot')
                                send_robot_action(robot,'stop')
                                # Robot stop

                        # ROBOT CONTROL 
                        
                        try: 
                            if stm_com == 1:
                                robot_status = 7
                                # Robot On Execution
                                if status == 1:
                                    print('file:', ctrl_commad, ' speed:',
                                            ctrl_speed, ' target_id:', target_id)
                                    robot.sync_program(start = 1)
                                    stm_com = 2
                                
                            if stm_com == 2:
                                robot_status = 7
                                if status == 3:
                                    if target_id < targets_len-1:
                                        target_id = target_id + 1
                                        robot.sync_setpoint(targets,target_id)
                                        robot.sync_program(start = 0)
                                        stm_com = 1
                                    else:
                                        print('routine complete, select another routine') 
                                        stm_com = 0
                        except:
                            print('Control Robot Error, stopping robot...')
                            send_robot_action(robot,'stop')
                    else:
                        print('robot status is incorrect...', robot_status)
                # ROBOT NOK   
                else:
                    try:
                        robot.connect()
                        robot.get_data()
                        send_robot_action(robot,'auto_init')
                        send_robot_action(robot,'auto_play')
                        send_robot_action(robot,'stop')
                        # if robot_status == 7:
                        #     send_robot_action(robot,'start')
                        #     print('Ready to Work!!!')

                    except:
                        print('Connection problem...')

                robot_data,_ = robot.get_data()
                _position = robot_data.get('actual_q') 
                _current = robot_data.get('actual_current') 
                _temperature = robot_data.get('joint_temperatures') 
                _tool = robot_data.get('output_int_register_1') 
                _execute = 0
                _resultwork = 0
                _status = 0
                
                mqtt.publish(publish_topics[2],robot_status)    
                mqtt.publish(publish_topics[4],_position)
                mqtt.publish(publish_topics[6],_current)
                mqtt.publish(publish_topics[8],_temperature)
                mqtt.publish(publish_topics[10],_tool)
                mqtt.publish(publish_topics[12],_execute)
                mqtt.publish(publish_topics[14],_resultwork)
                mqtt.publish(publish_topics[16],_status)
            
            #MQTT NOK
            else:
                if robot.robot_ok:    
                    # SEND STOP CONFIGURATION
                    print('Error getting MQTT data, stopping robot...')
                    robot.sync_config(slider_mask = 1, slider_fraction = 0)
                    send_robot_action(robot,'stop')
                    robot_data,robot_status = robot.get_data()

                mqtt.connect(subscribe_topics)
                received_msg = mqtt.get_data()
                mqtt.publish(publish_topics[0],0)
                

    except KeyboardInterrupt:
            robot.disconnect()
            time.sleep(1)
            print('Closing program...')
            sys.exit()
