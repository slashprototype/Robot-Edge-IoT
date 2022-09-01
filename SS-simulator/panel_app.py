#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk, font
from threading import Thread
import time
import numpy as np
import mqtt_con

global x_it
x_it = 0


class Application():

    def __init__(self, w_name):

        global running
        publish_topics = [
                    "/PCB/CELL-A/UR3-A/CONTROLLER/COMMAND/VALUE",
                    "/PCB/CELL-A/UR3-A/CONTROLLER/EXECUTE/VALUE",
                    "/PCB/CELL-A/UR3-A/CONTROLLER/EMERGENCYSTOP/VALUE",
                    "/PCB/CELL-A/UR3-A/CONTROLLER/SPEED/VALUE",
                    "/PCB/CELL-A/UR3-A/MONITORING/VISOR/VALUE",

                    "/PCB/CELL-B/UR3-B/CONTROLLER/COMMAND/VALUE",
                    "/PCB/CELL-B/UR3-B/CONTROLLER/EXECUTE/VALUE",
                    "/PCB/CELL-B/UR3-B/CONTROLLER/EMERGENCYSTOP/VALUE",
                    "/PCB/CELL-B/UR3-B/CONTROLLER/SPEED/VALUE",

                    "/PCB/CELL-A/UR3-A/MONITORING/VISOR/VALUE",
                    "/PCB/CELL-A/UR3-A/CONTROLLER/VISOR/VALUE"
                    
                    ]

        subscribe_topics = ["/PCB/CELL-A/UR3-A/MONITORING/STATUS/TYPE",
                            # "/PCB/CELL-A/UR3-A/MONITORING/STATUS/VALUE",
                            # "/PCB/CELL-A/UR3-A/CONTROLLER/JOBNUMBER/VALUE",
                            "/PCB/CELL-A/UR3-A/CONTROLLER/SPEED/VALUE",
                            # "/PCB/CELL-A/UR3-A/MONITORING/VISOR/VALUE",
                            # "/PCB/CELL-A/UR3-A/CONTROLLER/VISOR/VALUE",
                            "/PCB/CELL-A/UR3-A/CONTROLLER/COMMAND/VALUE",
                            # "/PCB/CELL-A/UR3-A/MONITORING/POSITION/VALUE",
                            # "/PCB/CELL-A/UR3-A/MONITORING/CURRENT/VALUE",
                            # "/PCB/CELL-A/UR3-A/MONITORING/TEMPERATURE/VALUE",
                            # "/PCB/CELL-A/UR3-A/CONTROLLER/TOOL/VALUE",
                            "/PCB/CELL-A/UR3-A/CONTROLLER/EXECUTE/VALUE",
                            "/PCB/CELL-A/UR3-A/CONTROLLER/RESULTWORK/VALUE",
                            "/PCB/CELL-A/UR3-A/CONTROLLER/STATUS/VALUE"
                            ]

        def initThread():
            global running
            running = True
            mqtt_thread.start()

        def close_app():
            global running
            running = False
            time.sleep(0.5)
            print('closing program')
        try:
            mqtt_thread.join(timeout=2)
        except:
            print('no thread1')

        def mqtt_loop():
            global running

            time.sleep(0.1)
            # Create broker client
            mqtt_con.mqtt_start('10.40.30.50', 31285, 30,
                                publish_topics, subscribe_topics)

            while(running):
                time.sleep(0.1)

                # mqtt_con.client.publish(publish_topics[0],self.rutina_A.get() ,1,True)
                # mqtt_con.client.publish(publish_topics[1],self.execute_A.get() ,1,True)
                mqtt_con.client.publish(publish_topics[2],self.emergency_A.get(),1,True)
                # mqtt_con.client.publish(publish_topics[3],"{:.2f}".format(self.speed_A.get()) ,1,True)
                # mqtt_con.client.publish(publish_topics[4],self.visor_trigger.get(),1,True)
                
                # mqtt_con.client.publish(publish_topics[5],self.rutina_B.get() ,1,True)
                # mqtt_con.client.publish(publish_topics[6],self.execute_B.get() ,1,True)
                # mqtt_con.client.publish(publish_topics[7],self.emergency_B.get() ,1,True)
                # mqtt_con.client.publish(publish_topics[8],"{:.2f}".format(self.speed_B.get()),1,True)
                
                # mqtt_con.client.publish(publish_topics[9],0 ,1,True)
                # mqtt_con.client.publish(publish_topics[10],0 ,1,True)
                # if len(mqtt_con.received_msg) > 0:
                #     print(mqtt_con.received_msg)
                # time.sleep(1)

            mqtt_thread.join(timeout=2)

        # RUTINA A ENTRY BOX
        def set_command_A():
            self.rutina_A.set(self.entry_A.get())
            mqtt_con.client.publish(publish_topics[0],self.rutina_A.get() ,1,True)
            # print(self.rutina.get())
        
        # RUTINA B ENTRY BOX
        def set_command_B():
            self.rutina_B.set(self.entry_B.get())
            # print(self.rutina.get())

        # SPEED A
        def set_speed_plus_A():
            self.speed_A.set(self.speed_A.get()+0.01)
            mqtt_con.client.publish(publish_topics[3],"{:.2f}".format(self.speed_A.get()) ,1,True)
            # print(self.speed.get())

        def set_speed_minus_A():
            if self.speed_A.get() > 0:
                self.speed_A.set(self.speed_A.get()-0.01)
                mqtt_con.client.publish(publish_topics[3],"{:.2f}".format(self.speed_A.get()) ,1,True)
                # print(self.speed.get())
        
        # SPEED B
        def set_speed_plus_B():
            self.speed_B.set(self.speed_B.get()+0.01)
            # print(self.rutina.get())

        def set_speed_minus_B():
            if self.speed_B.get() > 0:
                self.speed_B.set(self.speed_B.get()-0.01)
                # print(self.speed.get())
        
        def send_execute_A():
            mqtt_con.client.publish(publish_topics[1],1,1,True)
        
        def send_execute_B():
            mqtt_con.client.publish(publish_topics[5],1,1,True)
        
        
        def set_job():
            # mqtt_con.client.publish(publish_topics[4],self.entry_A.get(),1,True)
            mqtt_con.client.publish(publish_topics[1],1 ,1,True)
            
        mqtt_thread = Thread(target=mqtt_loop)

        self.raiz = Tk()
        self.raiz.configure(bg='beige')
        self.raiz.title(w_name)

        self.rutina_A = IntVar(value=0)
        self.speed_A = DoubleVar(value=0.0)
        self.modo_operacion_A = IntVar(value=0)
        self.speed_mode_A = IntVar(value=0)
        self.emergency_A = IntVar(value=0)
        self.gp_bool_65_A = IntVar(value=0)
        self.gp_bool_66_A = IntVar(value=0)
        self.gp_bool_67_A = IntVar(value=0)
        self.gp_bool_68_A = IntVar(value=0)
        self.execute_A = IntVar(value=0)
        self.visor_trigger = IntVar(value=0)

        self.rutina_B = IntVar(value=0)
        self.speed_B = DoubleVar(value=0.0)
        self.modo_operacion_B = IntVar(value=0)
        self.speed_mode_B = IntVar(value=0)
        self.emergency_B = IntVar(value=0)
        self.gp_bool_65_B = IntVar(value=0)
        self.gp_bool_66_B = IntVar(value=0)
        self.gp_bool_67_B = IntVar(value=0)
        self.gp_bool_68_B = IntVar(value=0)
        self.execute_B = IntVar(value=0)

        # Modo de operacion 0= Manual, 1=Automatico

        self.raiz.resizable(0, 0)

        style = ttk.Style(self.raiz)

        style.configure('My.TFrame', background='beige')

        style.configure('My.TLabel', foreground='black',
                        background='White', font=('Helvetica', 11), padding=(8, 8))

        style.configure('My.TButton', background='beige', borderwidth=10, width=8,
                        ipadx=100, pady=1, foreground='black', font=('Helvetica', 11), padding=(8, 8))

        # Define Marco Frames
        self.marcoLeft_0A = ttk.Frame(self.raiz, borderwidth=2,
                                     relief="raised", padding=(10, 10), style='My.TFrame')
        self.marcoLeft_1A = ttk.Frame(self.raiz, borderwidth=2,
                                     relief="raised", padding=(10, 10), style='My.TFrame')
        self.marcoLeft_2A = ttk.Frame(self.raiz, borderwidth=2,
                                     relief="raised", padding=(10, 10), style='My.TFrame')
        self.marcoRight_0A = ttk.Frame(self.raiz, borderwidth=2,
                                      relief="raised", padding=(10, 10), style='My.TFrame')
        
        self.marcoLeft_0B = ttk.Frame(self.raiz, borderwidth=2,
                                     relief="raised", padding=(10, 10), style='My.TFrame')
        self.marcoLeft_1B= ttk.Frame(self.raiz, borderwidth=2,
                                     relief="raised", padding=(10, 10), style='My.TFrame')
        self.marcoLeft_2B = ttk.Frame(self.raiz, borderwidth=2,
                                     relief="raised", padding=(10, 10), style='My.TFrame')
        self.marcoRight_0B = ttk.Frame(self.raiz, borderwidth=2,
                                      relief="raised", padding=(10, 10), style='My.TFrame')


        # Define Labels
        self.labelTitle_A = ttk.Label(self.marcoLeft_0A, text="ROBOT A", style='My.TLabel')
        self.labelTitle_B = ttk.Label(self.marcoLeft_0B, text="ROBOT B", style='My.TLabel')

        self.btn_routine_1_A = ttk.Button(self.marcoLeft_0A, text='Send',
                                        style='My.TButton', width=7, command=set_command_A)
        self.btn_routine_1_B = ttk.Button(self.marcoLeft_0B, text='Send',
                                        style='My.TButton', width=7, command=set_command_B)


        # BUTTONS SPEED A
        self.btn_speed_1_A = ttk.Button(self.marcoLeft_0A, text='speed ++',
                                      style='My.TButton', width=7, command=set_speed_plus_A)
        self.btn_speed_2_A = ttk.Button(self.marcoLeft_0A, text='speed --',
                                      style='My.TButton', width=7, command=set_speed_minus_A)

        # BUTTONS SPEED B
        self.btn_speed_1_B = ttk.Button(self.marcoLeft_0B, text='speed ++',
                                      style='My.TButton', width=7, command=set_speed_plus_B)
        self.btn_speed_2_B = ttk.Button(self.marcoLeft_0B, text='speed --',
                                      style='My.TButton', width=7, command=set_speed_minus_B)

        


        # MARCO3
        self.box_emergency_stop_A = ttk.Checkbutton(self.marcoLeft_1A, text='Emergency stop',
                                               variable=self.emergency_A,
                                               onvalue=1, offvalue=0)
        self.remote_speed_A = ttk.Checkbutton(self.marcoLeft_1A, text='spd',
                                            variable=self.speed_mode_A,
                                            onvalue=1, offvalue=0)
        self.check_execute_A = ttk.Checkbutton(self.marcoLeft_1A, text='execute',
                                            variable=self.execute_A,
                                            onvalue=1, offvalue=0)
        
        self.check_visor_trigger = ttk.Checkbutton(self.marcoLeft_1A, text='visor trigger',
                                            variable=self.visor_trigger,
                                            onvalue=170, offvalue=255)                                            
        self.entry_A = ttk.Entry(self.marcoLeft_1A)

        
        self.box_emergency_stop_B = ttk.Checkbutton(self.marcoLeft_1B, text='Emergency stop',
                                               variable=self.emergency_B,
                                               onvalue=1, offvalue=0)
        self.remote_speed_B = ttk.Checkbutton(self.marcoLeft_1B, text='spd',
                                            variable=self.speed_mode_B,
                                            onvalue=1, offvalue=0)

        self.check_execute_B = ttk.Checkbutton(self.marcoLeft_1B, text='execute',
                                            variable=self.execute_B,
                                            onvalue=1, offvalue=0)
        self.entry_B = ttk.Entry(self.marcoLeft_1B)
        
        # MARCO4
        self.btn_send_execute = ttk.Button(self.marcoLeft_2A, text='send execute',
                                      style='My.TButton', width=7, command=send_execute_A)

        self.btn_exit = ttk.Button(self.marcoLeft_2A, text='Salir',
                                   style='My.TButton', width=7, command=close_app)

        # Rigth Marco Frame
        self.marcoLeft_0A.grid(column=0, row=0)
        self.marcoLeft_1A.grid(column=0, row=2)
        self.marcoLeft_2A.grid(column=0, row=3)

        self.marcoLeft_0B.grid(column=2, row=0)
        self.marcoLeft_1B.grid(column=2, row=2)
        self.marcoLeft_2B.grid(column=2, row=3)

        # Marco 01
        self.labelTitle_A.grid(column=1,row=1)
        self.btn_routine_1_A.grid(column=1,row=2)
        self.btn_speed_1_A.grid(column=1, row=3)
        self.btn_speed_2_A.grid(column=0, row=3)
        
        self.labelTitle_B.grid(column=1,row=1)
        self.btn_routine_1_B.grid(column=1,row=2)
        self.btn_speed_1_B.grid(column=1, row=3)
        self.btn_speed_2_B.grid(column=0, row=3)

        # Marco 02
        self.box_emergency_stop_A.grid(column=0, row=0)
        self.remote_speed_A.grid(column=0, row=2)
        self.check_execute_A.grid(column=0, row=3)
        self.check_execute_A.grid(column=0, row=4)
        self.check_visor_trigger.grid(column=0, row= 5)
        self.entry_A.grid(column=0,row=6)

        self.box_emergency_stop_B.grid(column=0, row=0)
        self.remote_speed_B.grid(column=0, row=2)
        self.check_execute_B.grid(column=0, row=8)
        self.entry_B.grid(column=0,row=9)

        # Marco 04
        self.btn_exit.grid(column=2, row=0, padx=5, pady=5)
        self.btn_send_execute.grid(column=1, row=0, padx=5)

        # initThread()
        initThread()
        self.raiz.mainloop()


if __name__ == '__main__':
    app = Application('Super software simulator')
