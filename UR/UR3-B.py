from classes.robotUR import *
from main import robot_loop
import json

NAME = 'UR3-B'
ROBOT_IP = '10.40.30.11'

f = open(NAME + '.json',)
config = json.load(f)

SUBSCRIBE_TOPICS = []
PUBLISH_TOPICS = []

for i in config['SUBSCRIBE_TOPICS']:
    SUBSCRIBE_TOPICS.append(i)

for i in config['PUBLISH_TOPICS']:
    PUBLISH_TOPICS.append(i)

ROUTINES_PATH = 'routines/'+NAME+'_routines/'

robot = Robot(ROBOT_IP, NAME, 30004)
robot.connect_to_robot()
robot.start_rtde()
robot_loop(robot,NAME,SUBSCRIBE_TOPICS,PUBLISH_TOPICS,ROUTINES_PATH)