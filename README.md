# Robot-Edge-IoT

This project is a development for using RTDE protocol of Universal Robot Company for control and manipulating Robots like UR3,UR5 series. Is designed to work in a raspberry Pi 3,4 such a "Edge IoT"

## Features:

- Send monitoring data from robot to MQTT broker
- Include folder with the files needed by UR OS for run the selected program
- Use MQTT topics for receive commands and select the routine based on "/robot_name/routines" folder
- Atomatically initialize the robot and use watchdog security config

## Modules installation required

- `paho-mqtt`
- `rtde` module download at universal robot page
- `jsonpickle`

## Version 0.7

This version is functional, added new logic required for manage: Vision Sensor, Inspection Camera, Robot Moves, Robot tool actions

Manage retrying connection and last message sended to broker when disconnect from it
