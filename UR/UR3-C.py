import json
import sys
sys.path.append('classes/app/')
sys.path.append('classes/app/utils/')
sys.path.append('classes/mqtt/')
sys.path.append('classes/robotUR/')

from app import App
from mqtt import Mqtt
from robotUR import Robot

# Set parameters for configuration
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

# Parameters to create a robot instance
robot = Robot(ROBOT_IP, NAME, 30004, config_file)

# Parameters to create a mqtt client instance, 5 seconds to broker timeout
mqtt = Mqtt('10.40.30.50', 31285, 5,NAME)

# Create an App instance to start running the program with the respective robot
app = App(mqtt,robot,subscribe_topics,publish_topics,ROUTINES_PATH)