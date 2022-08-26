import sys
import time
import text_processor

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

def update_once(mqtt,publish_topic,value):
    mqtt.publish(publish_topic,value)

def get_fsm_status_type(fsm_id):
    types = {
        0:'Control algorithm not initialized',
        10:'reset routine',
        20:'Starting normal control loop',
        21:'Waiting for execute',
        22:'Checking index and move type',
        23:'Send actual target and start = 1 to robot',
        24:'increase index and start = 0 to robot',
        40:'Special Move type detected, alternative routine',
        30:'Alarm status, check for reset or another anomaly'
    }
    return types[fsm_id]


