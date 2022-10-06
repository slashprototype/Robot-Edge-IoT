import sys
sys.path.append('classes/app/')
sys.path.append('classes/app/utils/')
sys.path.append('classes/mqtt/')
sys.path.append('classes/robotUR/')


from app import App
from mqtt import Mqtt
from robotUR import Robot

import json

NAME = 'UR3-C'
ROBOT_IP = '10.7.7.13'
config_file = 'configuration/configuration.xml'

topics_file = open('configuration/'+NAME+'.json',)
topics_json = json.load(topics_file)

SUBSCRIBE_TOPICS_DICTIONARY = topics_json.get('SUBSCRIBE_TOPICS')
PUBLISH_TOPICS_DICTIONARY = topics_json.get('PUBLISH_TOPICS')

subscribe_topics = {}
publish_topics = {}


for key,value in SUBSCRIBE_TOPICS_DICTIONARY.items():
    subscribe_topics[key] = value

for key,value in PUBLISH_TOPICS_DICTIONARY.items():
    publish_topics[key] = value

ROUTINES_PATH = 'routines/'+NAME+'_routines/'

robot = Robot(ROBOT_IP, NAME, 30004, config_file)

mqtt = Mqtt('inginx.icidesi.mx', 8883, 10,NAME)

app = App(mqtt,robot,subscribe_topics,publish_topics,ROUTINES_PATH)