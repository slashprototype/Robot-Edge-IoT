import time
from datetime import datetime
import sys
from classes.app.app import App
from classes.mqtt.mqtt import Mqtt
from classes.robotUR.robotUR import Robot

app = App('broker','UR3-A','subscrib','publish','path')
# def __init__(self, mqtt,robot,subscribe_topics,publish_topics,routines_path):
