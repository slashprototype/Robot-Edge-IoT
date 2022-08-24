from shutil import ExecError
import sys
import rtde.rtde_config as rtde_config
import rtde.rtde as rtde
import argparse
import logging
import jsonpickle
import json
import time
import os

class Robot():

    def __init__(self, ip,name, port, config_file):
        # parameters
        self.name = name
        self.ip = ip
        self.connection_status = False
        self.alarm = 'Not connected'
        self.alarm_id = 0

        parser = argparse.ArgumentParser()
        parser.add_argument('--host', default=ip,
                            help='name of host to connect to ip')
        parser.add_argument('--port', type=int, default=port,
                            help='port number (30004)')
        parser.add_argument('--samples', type=int, default=0,
                            help='number of samples to record')
        parser.add_argument('--frequency', type=int, default=125,
                            help='the sampling frequency in Herz')
        parser.add_argument('--config', default=config_file,
                            help='data configuration file to use ')
        parser.add_argument(
            "--verbose", help="increase output verbosity", action="store_true")
        parser.add_argument(
            "--buffered", help="Use buffered receive which doesn't skip data", action="store_true")
        parser.add_argument(
            "--binary", help="save the data in binary format", action="store_true")
        self.args = parser.parse_args()
        self.conf = rtde_config.ConfigFile(self.args.config)

        if self.args.verbose:
            logging.basicConfig(level=logging.INFO)
        # logging.getLogger().setLevel(logging.INFO)
        print('Getting configuration new robot instance')
        time.sleep(0.5)
        self.robot_info_names, self.robot_info_types = self.conf.get_recipe('robot_info')
        self.control_input_names, self.control_input_types = self.conf.get_recipe('control_input')
        self.watchdog_names, self.watchdog_types = self.conf.get_recipe('watchdog')
        self.slider_names, self.slider_types = self.conf.get_recipe('slider')
        self.program_input_names, self.program_input_types = self.conf.get_recipe('program_input')
        self.setpoint_names, self.setpoint_types = self.conf.get_recipe('setpoint')
        self.setpoint_vars_names, self.setpoint_vars_types = self.conf.get_recipe('setpoint_vars')
        print('A robot named:',self.name, 'at ip:', self.ip, 'Has been created correctly')
        time.sleep(0.5)

    def connect(self):
        print('connecting to robot...')
        time.sleep(0.5)
        try:
            self.con = rtde.RTDE(self.args.host, self.args.port)
            self.con.connect()
            self.con.get_controller_version()
            try:
                # setup recipes
                self.robot_info = self.con.send_output_setup(self.robot_info_names, self.robot_info_types, frequency=self.args.frequency)
                self.control_input = self.con.send_input_setup(self.control_input_names, self.control_input_types)
                self.watchdog = self.con.send_input_setup(self.watchdog_names, self.watchdog_types)
                self.slider = self.con.send_input_setup(self.slider_names, self.slider_types)
                self.program_input = self.con.send_input_setup(self.program_input_names, self.program_input_types)
                self.setpoint = self.con.send_input_setup(self.setpoint_names, self.setpoint_types)
                self.setpoint_vars = self.con.send_input_setup(self.setpoint_vars_names, self.setpoint_vars_types)   
                print('succesfully connected to '+self.ip)
            except:
                self.connection_status = False
                self.alarm_id = 1
                raise Exception('error in setup recipes')

            self.initial_control_values()
            if not self.con.send_start():
                self.connection_status = False
                self.alarm_id = 2
                raise Exception('Unable to start rtde synchronization')
            else:
                self.connection_status = True
                self.alarm_id = 0
                print('rtde syncronized correctly!')  

        except:
            if os.system("ping -c 1 -w2 " + self.ip) == 0:
                self.disconnect()
                self.connection_status = False
                self.alarm = 'Unable to create a connection, check robot alarm_id: '+ str(self.alarm_id)
            else:
                self.connection_status = False
                self.alarm = 'Unable to find a robot at '+self.ip


    def initial_control_values(self):
        # Control input
        self.control_input.input_bit_register_64 = 0
        self.control_input.input_bit_register_65 = 0
        self.control_input.input_bit_register_66 = 0
        self.control_input.input_bit_register_67 = 0
        self.control_input.input_bit_register_68 = 0
        self.control_input.input_bit_register_69 = 0

        # Watchdog
        self.watchdog.input_int_register_0 = 0

        # Slider (slider mask [0 = don't apply this value in teach,1 = user speed_slider_fraction])
        # speed slider fraction = percentage of speed in each move, 1 is 100%
        self.slider.speed_slider_mask = 1
        self.slider.speed_slider_fraction = 0

        # Program input (start,target_id_in,script_id_in)
        self.program_input.input_int_register_1 = 0
        self.program_input.input_int_register_2 = 0
        self.program_input.input_int_register_3 = 0

        # setpoint
        self.setpoint.input_double_register_0 = 0
        self.setpoint.input_double_register_1 = 0
        self.setpoint.input_double_register_2 = 0
        self.setpoint.input_double_register_3 = 0
        self.setpoint.input_double_register_4 = 0
        self.setpoint.input_double_register_5 = 0

        # setpoint_vars(accel, speed, blend_radius_m)
        self.setpoint_vars.input_double_register_20 = 0
        self.setpoint_vars.input_double_register_21 = 0
        self.setpoint_vars.input_double_register_22 = 0
        self.setpoint_vars.input_int_register_20 = 0


    def sync_control(self, action, value):
        # control input
        if action == 'auto_init':
            self.control_input.input_bit_register_64 = value
        if action == 'auto_play':
            self.control_input.input_bit_register_65 = value
        if action == 'start':
            self.control_input.input_bit_register_66 = value
        if action == 'stop':
            self.control_input.input_bit_register_67 = value
        if action == 'pause':
            self.control_input.input_bit_register_68 = value
        if action == 'freedrive':
            self.control_input.input_bit_register_69 = value
        
        self.con.send(self.control_input)


    def sync_config(self,**args):
        # watchdog
        # slider
        for key,value in args.items():
            if key == 'slider_mask':
                self.slider.speed_slider_mask = value
            if key == 'slider_fraction':
                self.slider.speed_slider_fraction = value
            if key == 'watchdog':
                # print('watchdog in',self.name)
                self.watchdog.input_int_register_0 = value

        self.con.send(self.slider)
        self.con.send(self.watchdog)

    def sync_program(self,**args):

        for key,value in args.items():
            if key == 'start':
                self.program_input.input_int_register_1 = value
            if key == 'target_id_in':
                self.program_input.input_int_register_2 = value
            if key == 'script_id_in':
                self.program_input.input_int_register_3 = value

        self.con.send(self.program_input)


    def sync_setpoint(self, targets,target_id):

        def setp_to_list(setp):
            list = []
            for i in range(0, 6):
                list.append(setp.__dict__["input_double_register_%i" % i])
            return list

        def list_to_setp(setp, list):
            for i in range(0, 6):
                setp.__dict__["input_double_register_%i" % i] = list[i]
            return setp

        target = targets[target_id][0]
        accel = targets[target_id][1]
        speed = targets[target_id][2]
        blend_radius_m = targets[target_id][4]
        move_type = targets[target_id][5]

        # (speed, accel, blend_radius_m, move_type)
        self.setpoint_vars.input_double_register_20 = accel
        self.setpoint_vars.input_double_register_21 = speed
        self.setpoint_vars.input_double_register_22 = blend_radius_m
        self.setpoint_vars.input_int_register_20 = move_type

        # print('actual target is: ',target)
        new_setpoint = target
        self.setpoint = list_to_setp(self.setpoint, new_setpoint)
        self.con.send(self.setpoint)
        self.con.send(self.setpoint_vars)
        # print('target pos: ', setp_to_list(self.setpoint),' speed: ',speed, ' crtl spd: ',self.slider.speed_slider_fraction)

    def get_data(self):
        robot_status = 0
        
        try:
            if self.args.buffered:
                self.state = self.con.receive_buffered(self.args.binary)
            else:
                self.state = self.con.receive(self.args.binary)
            
            data = jsonpickle.encode(self.state)
            robot_data = json.loads(data)
            # for i in robot_data.items():
            #     print(i)
            robot_mode = robot_data.get('robot_mode')
            safety_status = robot_data.get('safety_status')
            
            if safety_status == 1:

                if robot_mode == 2 or robot_mode == 4 or robot_mode == 5:
                    robot_status = 4
                if robot_mode == 3:
                    robot_status = 3
                if robot_mode == 7:
                    robot_status = 6

            elif safety_status == 3:
                robot_status = 2

            elif safety_status == 7:
                robot_status = 1

            self.connection_status = True
            return (robot_data,robot_status)

        # except rtde.RTDEException:
        except:
            self.connection_status = False
            print('problem getting data...')
            raise Exception('problem getting data...')
        
        

    def disconnect(self):
        self.connection_status = False
        self.con.send_pause()
        self.con.disconnect()