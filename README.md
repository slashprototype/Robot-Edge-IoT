# Robot-Edge-IoT

This project is a development for using RTDE protocol of Universal Robot Company for control and manipulating Robots like UR3,UR5 series. Is designed to work in a raspberry Pi 3,4 such a "Edge IoT"

## Version 1.0

### Features:

- Include folder with the files needed by UR OS for run the selected program
- Use MQTT topics for receive commands and select the routine based on /routines folder
- Atomatically initialize the robot and use watchdog security config

# Modules Required

- `paho-mqtt`
- `rtde` module download at universal robot page
- `jasonpickle`
