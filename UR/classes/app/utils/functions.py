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
            if i == 10:
                robot.sync_control(action,0)
            if i == 20:
                running = False
            else:
                i = i + 1
    except KeyboardInterrupt:
        pass
    except:
        print('problem in robot connection')

def search_script(robot_name,command):
        type_receipt = {'1':'MOVE','2':'PICK','3':'PLACE','4':'SNAP'}
        str_command = str(command)
        file = ''
        station =   str_command[0] 
        type = str_command[1]
        robot_name_ID = robot_name[len(robot_name)-1]
        file = 'R'+robot_name_ID+'_E'+station+'_'+type_receipt[type]+'_'+str_command+'.script'
        return (file)

def get_robot_targets(file):
    targets = text_processor.process(file)
    targets_len = len(targets)
    return (targets,targets_len)