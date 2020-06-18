#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 18:57:38 2020

@author: tydar
"""


import pyfirmata
import time
import Controls

class Arduino_Control:
    def __init__(self,SerialPort,MotorPin,LightPin,ServoPin,BuzzerPin):
        self.board = pyfirmata.Arduino(SerialPort)
        self.it = pyfirmata.util.Iterator(self.board)
        self.it.start()
        
        MotorPin_Str = ''.join(['d:',str(MotorPin),':p'])
        self.Shutter_Motor = self.board.get_pin(MotorPin_Str)
        self.Shutter_Motor.write(0)
        
        OpenLight_Str = ''.join(['d:',str(LightPin),':o'])
        self.Open_Light = self.board.get_pin(OpenLight_Str)
        
        ServoPin_Str = ''.join(['d:',str(ServoPin),':s'])
        self.Servo = self.board.get_pin(ServoPin_Str)
        self.Servo.write(0)
        
#         BuzzerPin_Str = ''.join(['d:',str(BuzzerPin),':p'])
#         self.Buzzer = self.board.get_pin(BuzzerPin_Str)
        
    def Open_ThermalColumn(self):
        try:
            self.Shutter_Motor.write(1)
#             self.Buzzer.write(.5)
            time.sleep(2)
            self.Servo.write(170)   
            self.Open_Light.write(1)
            self.Shutter_Motor.write(0)
#             self.Buzzer.write(0)
            time.sleep(0.1)
        except:
            Controls.SerialConnection_Error()
#             messagebox.showinfo("Communication Error",
#                                 "Serial Connection Lost! Restart this Application to Reconnect.")
            
    def Close_ThermalColumn(self):
        try:
            self.Shutter_Motor.write(1)
            self.Servo.write(0)
            self.Open_Light.write(0)
            self.Shutter_Motor.write(0)
        except:
            Controls.SerialConnection_Error()