import sys
sys.path.append('classes/app/')
sys.path.append('classes/app/utils/')
sys.path.append('classes/mqtt/')
sys.path.append('classes/robotUR/')


from app import App
from mqtt import Mqtt
from robotUR import Robot
from functions import search_script,send_robot_action,get_robot_targets

import json

NAME = 'UR3-A'
ROBOT_IP = '10.40.30.11'
config_file = 'configuration/configuration.xml'

topics_file = open('configuration/'+NAME+'.json',)
topics = json.load(topics_file)

SUBSCRIBE_TOPICS = []
PUBLISH_TOPICS = []

for i in topics['SUBSCRIBE_TOPICS']:
    SUBSCRIBE_TOPICS.append(i)

for i in topics['PUBLISH_TOPICS']:
    PUBLISH_TOPICS.append(i)

ROUTINES_PATH = 'routines/'+NAME+'_routines/'

robot = Robot(ROBOT_IP, NAME, 30004, config_file)

mqtt = Mqtt('10.40.30.50', 31285, 30,NAME)

app = App(mqtt,robot,SUBSCRIBE_TOPICS,PUBLISH_TOPICS,ROUTINES_PATH)