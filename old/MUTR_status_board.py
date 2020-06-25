#!/usr/bin/env python
# coding: utf-8
"""
An interactive status board for the Maryland University Training Reactor (MUTR)
This program will be deprecated after the code restructuring

This status board:
    - Tracks fuel bundle location

@author: Telon Yan, Michael Van Selous
"""
# In[1]: imports

import tkinter as tk
from tkinter import messagebox
import csv
import pyfirmata
import time

# In[2]: Initializing variables


COLOR_DICT ={"Fuel Bundle":'#3F3B35', "Fuel Element":'#1E3A95',
             "IR":'#B0BC00', "CR 1":'#2DB3D8',
             "CR 2":'#2DB3D8', "RR":'#2F958C',
             "PuBe Source":'#44CA3A', "CIC":'#AB3674',
             "FC":'#A41919', "IC":'#6E5F15',
             "Rabbit":'#CA1FC7', "Reflector":'#807C8B',
             "Beam Port":'#CACACA', "Thermal Column":'#CACACA',
             "Through Tube":'#CACACA', "Storage":'#A8A8A8',
             "Storage_Element":'#A5D920', "Open Thermal Column":'#1A7A18',
             "Close Thermal Column":'#822A08', "Rack":'grey',
             "Restore Serial":'#69A1AB', "Remove Fuel":'#3A9358',
             "Return Fuel":'#3A9358', "Select Element":'grey',
             "Select Container":'grey', "Beam Port 1":'#AB6330',
             "Beam Port 2":'#AB6330'}


# In[3]: Initalizing variables related to fuel element data


#Importing fuel_elements.csv data
FUEL_ELEMENT_DATA_DICT = {}
with open('fuel_elements.csv', encoding='utf-8-sig') as fuel_element_data:
    read_fuel_element_data = csv.reader(fuel_element_data, delimiter=',')
    for row in read_fuel_element_data:
        FUEL_ELEMENT_DATA_DICT[row[0]] = [ row[1],row[2],row[3],row[4] ]

FUEL_ELEMENT_COORDS = {0:[57,57,1,1,29,29],
                 1:[61,57,117,1,89,29],
                 2:[57,61,1,117,29,89],
                 3:[61,61,117,117,89,89]}


# In[4]: Initializing variables related to core geometry


#Importing Core Geometry
MODULE = []
UNIT = []
X1 = []
Y1 = []
X2 = []
Y2 = []
STATE = []
fuel_states = {}

with open('core_geometry.csv', encoding='utf-8-sig') as core_geometry_data:
    read_core_geometry_data = csv.reader(core_geometry_data, delimiter=',')
    for row in read_core_geometry_data:
        MODULE.append(row[0])
        UNIT.append(row[1])
        X1.append(row[2])
        Y1.append(row[3])
        X2.append(row[4])
        Y2.append(row[5])
        STATE.append(row[6])

        # Dictionary of fuel bundles mapped to where they are
        if row[6]:
            fuel_states[row[1]] = row[6]

bundle_widgets_dict = {}
container_dict = {}


# In[5]: initializing variables related to control widgets


#Importing dictionary of buttons
CONTROL_DICT = {}
with open('control_widgets.csv', encoding='utf-8-sig') as control_widget_data:
    read_control_widget_data = csv.reader(control_widget_data, delimiter=',')
    for row in read_control_widget_data:
        CONTROL_DICT[int(row[0])] = [row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]]


# In[6]: Class to draw objects


class CreateCoreCanvas: #would like to update name
    def draw_reactor(canvas,module,unit,x1,y1,x2,y2):
        if module == "Fuel Bundle":
            bundle_widgets_dict[unit] = tk.Canvas(core_canvas,width = 118, height = 118,
                                                   bg = COLOR_DICT["Fuel Bundle"],
                                                   highlightthickness=0)
            #Once we have a location for the new fuel, this can be easily generalized
            #by simply removing the if statment.
            if "New" not in unit:
                canvas.create_rectangle(int(x1),int(y1),int(x2),int(y2),
                                        fill = COLOR_DICT["Fuel Bundle"])
                canvas.create_oval(int(x1)+10,int(y1)+10,int(x2)-10,int(y2)-10,
                                   fill = COLOR_DICT["Rack"])
                canvas.create_text(int((int(x1)+int(x2))/2),int((int(y1)+int(y2))/2),
                                   text=unit,font=("Verdana", 16))
                bundle_widgets_dict[unit].X = int(x1)
                bundle_widgets_dict[unit].Y = int(y1)

            bundle_widgets_dict[unit].C_c_X = 60
            bundle_widgets_dict[unit].C_c_Y = 60
            for i in range(0,4):
                text = FUEL_ELEMENT_DATA_DICT[unit][i]
                if text in ["CR 1","RR","CR 2","IR"]:
                    color = COLOR_DICT[text]
                else:
                     color = COLOR_DICT["Fuel Element"]
                bundle_widgets_dict[unit].create_oval(FUEL_ELEMENT_COORDS[i][0],FUEL_ELEMENT_COORDS[i][1],
                                                          FUEL_ELEMENT_COORDS[i][2],FUEL_ELEMENT_COORDS[i][3],
                                                          fill = color)
                bundle_widgets_dict[unit].create_text(FUEL_ELEMENT_COORDS[i][4],FUEL_ELEMENT_COORDS[i][5],
                                                          text=text,font = (8))

        else:
            color = COLOR_DICT[module]
            if module in ["Reflector","Beam Port","Thermal Column","Through Tube","Rabbit","Storage"]:
                canvas.create_rectangle(int(x1),int(y1),
                                            int(x2),int(y2),
                                            fill = color)
            if module in ["PuBe Source","CIC","FC","IC"]:
                canvas.create_oval(int(x1),int(y1),
                                       int(x2),int(y2),
                                       fill = color)
            canvas.create_text( (int(x1)+int(x2))/2, (int(y1)+int(y2))/2,
                               text=''.join([module," ",unit]),font = ("Verdana",10,"bold") )

        if module == "Storage":
            bundle_widgets_dict[unit] = tk.Canvas(core_canvas,width = 80, height = 80,
                                         bg = COLOR_DICT["Storage_Element"],
                                         highlightthickness=0)
            bundle_widgets_dict[unit].X = int(x1)+8
            bundle_widgets_dict[unit].Y = int(y1)+8
            bundle_widgets_dict[unit].C_c_X = 40
            bundle_widgets_dict[unit].C_c_Y = 40

    def draw_fuel(unit,state):
        if state.isnumeric() == True:
            bundle_widgets_dict[state].create_text(bundle_widgets_dict[state].C_c_X,
                                                   bundle_widgets_dict[state].C_c_Y,
                                                   text=str(unit),font=("Verdana",10,"bold"))
            bundle_widgets_dict[state].place(x=bundle_widgets_dict[state].X,
                                             y=bundle_widgets_dict[state].Y)
            #Can be easaly generalized by removing if statement
            # FUel bundles placed in storage at the onset and not "new 1-5" get a return button
            if "New" not in unit:
                for i in range(0,len(buttons)):
                     if (buttons[i].module == "Return Fuel" and buttons[i].key == state):
                        buttons[i].the_button.place(x=buttons[i].x1,y=buttons[i].y1)
                        button_hit = i
                        container_dict[state] = [unit,button_hit]
        else:
            bundle_widgets_dict[state].place(x=bundle_widgets_dict[state].X,
                                             y=bundle_widgets_dict[state].Y)



# In[7]:


class ArduinoControl:
    def __init__(self,serial_port,motor_pin,light_pin,servo_pin,buzzer_pin):
        self.board = pyfirmata.Arduino(serial_port)
        self.it = pyfirmata.util.Iterator(self.board)
        self.it.start()

        motor_pin_str = ''.join(['d:',str(motor_pin),':p'])
        self.Shutter_Motor = self.board.get_pin(motor_pin_str)
        self.Shutter_Motor.write(0)

        open_light_str = ''.join(['d:',str(light_pin),':o'])
        self.Open_Light = self.board.get_pin(open_light_str)

        servo_pin_str = ''.join(['d:',str(servo_pin),':s'])
        self.Servo = self.board.get_pin(servo_pin_str)
        self.Servo.write(0)

#         BuzzerPin_Str = ''.join(['d:',str(buzzer_pin),':p'])
#         self.Buzzer = self.board.get_pin(BuzzerPin_Str)

    def open_thermal_column(self):
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

    def close_thermal_column(self):
        try:
            self.Shutter_Motor.write(1)
            self.Servo.write(0)
            self.Open_Light.write(0)
            self.Shutter_Motor.write(0)
        except:
            Controls.SerialConnection_Error()


# In[8]:


class Controls:
    # canvas = Canvas button's placed on, module = button text, font = font size, key = location key
    def __init__(self,canvas,module,init_state,x1,y1,width,height,font,key):
        self.key = key
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.module = module

        #the_command becomes an anonymous function b/c of lambda
        if module == "Select Element":  #for fuel bundles in reactor
            text = "Select"
            the_command = lambda :Controls.bundle_selected(key)
        elif module =="Select Container": #for placing fuel in storage
            text = "Select"
            the_command = lambda :Controls.container_selected(key)
        elif module =="Return Fuel":    #for fuel in storage
            text = "Return"
            the_command = lambda :Controls.return_fuel(key)
        else:
            text = self.module
            the_command = COMMAND_DICT[self.module]

        # make the button
        self.the_button = tk.Button(canvas, bg=COLOR_DICT[self.module],
                                 command = the_command,
                                 text=text,font = ("Purisa", font),
                                 width = width,
                                 height = height)
        self.the_button.place(x=self.x1,y=self.y1)
        if init_state == "Hidden":
            self.the_button.place_forget()

    def SerialConnection_Error():
        messagebox.showinfo("Communication Error",
                            "Serial Connection Lost. Restart this Application and Reconnect.")

    #after clicking "remove fuel"
    def remove_fuel():
        #show the buttons with fuel in those places
        for i in range(0,len(buttons)):
            if (buttons[i].module == "Select Element"
                and fuel_states[buttons[i].key] == buttons[i].key):
                buttons[i].the_button.place(x=buttons[i].x1,y=buttons[i].y1)
            #stop showing [return] buttons for fuel in storage
            elif buttons[i].module == "Return Fuel":
                buttons[i].the_button.place_forget()

        messagebox.showinfo("Remove Fuel","Select Target Fuel Bundle")

    #after clicking a fuel element in reactor to remove
    def bundle_selected(key):
        global Bundle_Key
        Bundle_Key = key
        bundle_widgets_dict[key].place_forget()
        #stop showing all fuel in reactor, show fuel in
        for i in range(0,len(buttons)):
            if buttons[i].module == "Select Element":
                buttons[i].the_button.place_forget()
            #show unfilled storage buttons
            elif (buttons[i].module == "Select Container" and
                  buttons[i].key not in fuel_states.values()):
                buttons[i].the_button.place(x=buttons[i].x1,y=buttons[i].y1)

        messagebox.showinfo("Remove Fuel", "Select Destination")

    #after clicking a storage container to place fuel
    def container_selected(key):
        #makeother buttons disappear & place new button for new fuel in storage
        for i in range(0,len(buttons)):
            #remove all the "select" buttons
            if buttons[i].module == "Select Container":
                buttons[i].the_button.place_forget()
            #put back all the return buttons that have stuff & change fuel state
            elif buttons[i].module == "Return Fuel":
                #for the fuel that was just placed
                if buttons[i].key == key:
                    button_hit = i
                    fuel_states[Bundle_Key] = key
                #for return buttons
                if buttons[i].key in fuel_states.values():
                    buttons[i].the_button.place(x=buttons[i].x1,y=buttons[i].y1)

        bundle_widgets_dict[key].place(x=bundle_widgets_dict[key].X,
                                       y=bundle_widgets_dict[key].Y)
        bundle_widgets_dict[key].create_text(bundle_widgets_dict[key].C_c_X,
                                             bundle_widgets_dict[key].C_c_Y,
                                               text=Bundle_Key,font=("Verdana",10,"bold"))
        container_dict[key] = [Bundle_Key,button_hit]

    #after clicking a fuel in storage
    def return_fuel(key):
        Bundle = container_dict[key][0]
        fuel_states[Bundle] = Bundle
        button_hit = container_dict[key][1] #different than the bucket number.
                                            #Tagged based off order of creation.
        bundle_widgets_dict[Bundle].place(x=bundle_widgets_dict[Bundle].X,
                                             y=bundle_widgets_dict[Bundle].Y)
        bundle_widgets_dict[key].place_forget()
        buttons[button_hit].the_button.place_forget()
        del container_dict[key]

    def beam_port1():
        print("Need BP1")
    def beam_port2():
        print("Need BP2")
    def rabbit():
        print("Need Rabbit")
    def through_tube():
        print("Need TT")


# In[9]: essentially the "main"


master = tk.Tk()
canvas_width = 1920
canvas_height = 1080

master.title("MUTR Status Board")

# Create the canvases
core_canvas = tk.Canvas(master,width = 1400,height = canvas_height, bg = 'grey')
control_canvas = tk.Canvas(master,width = canvas_width-1400,height=canvas_height, bg = 'grey')

#add all the modules (shapes)
for i in range(1,len(MODULE)):
    CreateCoreCanvas.draw_reactor(core_canvas,MODULE[i],UNIT[i],X1[i],Y1[i],X2[i],Y2[i])

#see if arduino is connected and try giving functionality to the thermal column buttons
COMMAND_DICT = {}

try:
    arduino = ArduinoControl("COM5",3,8,11,3)
    COMMAND_DICT = {"Open Thermal Column":arduino.open_thermal_column,
                    "Close Thermal Column":arduino.close_thermal_column}
except:
    COMMAND_DICT = {"Open Thermal Column":Controls.SerialConnection_Error,
                    "Close Thermal Column":Controls.SerialConnection_Error}
    messagebox.showinfo("Unable to Establish Serial Connection!",
                        "Please verify your device is connected to 'COM5' then restart the Application")


# TODO - Dictionary of commands for buttons - confusing placement
COMMAND_DICT.update({"Remove Fuel":Controls.remove_fuel,
                     "Beam Port 1":Controls.beam_port1,
                     "Beam Port 2":Controls.beam_port2,
                     "Rabbit":Controls.rabbit,
                     "Through Tube":Controls.through_tube})

CANVAS_DICT = {"Core_Canvas":core_canvas,"Control_Canvas":control_canvas}

# makes buttons by instantiating i # objects of the Controls class
buttons = []
for i in range(1,len(CONTROL_DICT)):
    buttons.append(Controls(CANVAS_DICT[CONTROL_DICT[i][0]],CONTROL_DICT[i][1],CONTROL_DICT[i][2],CONTROL_DICT[i][3],
                   CONTROL_DICT[i][4],CONTROL_DICT[i][5],CONTROL_DICT[i][6],CONTROL_DICT[i][7],CONTROL_DICT[i][8]))

# FIXME this is hard coded and draw_fuel is kind of redundant
for i in range(1,25):
    CreateCoreCanvas.draw_fuel(UNIT[i],STATE[i])

core_canvas.grid(row=0,column=0)
control_canvas.grid(row=0,column=1)

master.update_idletasks()
master.update()
master.mainloop()


# In[10]: Close arduino connection


#Ensuring the shutter is closed sfter closing the application
"""
try:
    arduino.Open_Light.write(0)
    arduino.Shutter_Motor.write(0)
    arduino.Servo.write(0)
    time.sleep(1.5)
    arduino.board.exit()
except:
    messagebox.showinfo("Serial Connection Error","The serial connection was lost prior to closing the application\nPlease verify the shutter is closed.")
"""

# In[11]: Save configuration for next startup


#Saving/Exporting Current Fuel Locations for the next startup.
# container_dict
# {Bucket number: [Bundle,return button num]}


#We can now use this dict to update the Core_Geometry Spreadsheet!
    #Need to learn how to format outputs so I dont ruin destination file.
#print(container_dict)
