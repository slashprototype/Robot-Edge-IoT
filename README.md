# Robot-Edge-IoT

This project is a development for using RTDE protocol of Universal Robot Company for control and manipulating Robots like UR3,UR5 series. Is designed to work in a raspberry Pi 3,4 such a "Edge IoT"

## Features:

- Send monitoring data from robot to MQTT broker
- Include folder with the files needed by UR OS for run the selected program
- Use MQTT topics for receive commands and select the routine based on /routines folder
- Atomatically initialize the robot and use watchdog security config

## Modules Required

- `paho-mqtt`
- `rtde` module download at universal robot page
- `jasonpickle`

### Version 1.0

Functionall, still with no sendind the required data to mqtt

### Version 1.1

- Working in add publish topics correctly
- Generic topics for both robots defined and publish, execution logic isn't defined yet
- main.py was fixed and improved

### Version 1.2

- Will change the paradigm for run main logic by using an application in OOP, this changes are neccesary for using two main threads for robot control and mqtt functionality
- An "Aplication" class was created for replace old main.py
