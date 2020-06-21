#!/usr/bin/env python
# coding: utf-8
"""
An interactive status board for the Maryland University Training Reactor (MUTR)

This status board:
    - Tracks fuel bundle location

Additional desired functionality:
    - Track experiments taking place (samples in thermal column, rabbit, etc)
    - Perform arduino experiments (interface with Arduino loaded with experiment code)
        - Show serial output in window, ability to save to csv
    - save and load configurations as csvs

@author: Telon Yan, Michael Van Selous
"""
# In[1]: imports


import tkinter as tk
from tkinter import messagebox
import csv
import pyfirmata
import time

# In[2]: Initializing variables


color_dict ={"Fuel Bundle":'#3F3B35', "Fuel Element":'#1E3A95',
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
fuel_element_data_dict = {}
with open('fuel_elements.csv', encoding='utf-8-sig') as fuel_element_data:
    read_fuel_element_data = csv.reader(fuel_element_data, delimiter=',')
    for row in read_fuel_element_data:
        fuel_element_data_dict[row[0]] = [ row[1],row[2],row[3],row[4] ]

fuel_element_coords = {0:[57,57,1,1,29,29],
                 1:[61,57,117,1,89,29],
                 2:[57,61,1,117,29,89],
                 3:[61,61,117,117,89,89]}


# In[4]: Initializing variables related to core geometry


#Importing Core Geometry
module = []
unit = []
x1 = []
y1 = []
x2 = []
y2 = []
state = []
fuel_states = {}

with open('core_geometry.csv', encoding='utf-8-sig') as CoreGeometry_Data:
    read_CoreGeometry_Data = csv.reader(CoreGeometry_Data, delimiter=',')
    for row in read_CoreGeometry_Data:
        module.append(row[0])
        unit.append(row[1])
        x1.append(row[2])
        y1.append(row[3])
        x2.append(row[4])
        y2.append(row[5])
        state.append(row[6])

        # Dictionary of fuel bundles mapped to where they are
        if row[6]:
            fuel_states[row[1]] = row[6]

bundle_widgets_dict = {}
container_dict = {}


# In[5]: initializing variables related to control widgets


#Importing dictionary of buttons
Control_Dict = {}
with open('control_widgets.csv', encoding='utf-8-sig') as ControlWidget_Data:
    read_ControlWidget_Data = csv.reader(ControlWidget_Data, delimiter=',')
    for row in read_ControlWidget_Data:
        Control_Dict[int(row[0])] = [ row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]  ]


# In[6]:


class Create_Core_Canvas: #would like to update name
    def Draw_Reactor(canvas,module,unit,x1,y1,x2,y2):
        if module == "Fuel Bundle":
            bundle_widgets_dict[unit] = tk.Canvas(Core_Canvas,width = 118, height = 118,
                                                   bg = color_dict["Fuel Bundle"],
                                                   highlightthickness=0)
            #Once we have a location for the new fuel, this can be easily generalized
            #by simply removing the if statment.
            if "New" not in unit:
                canvas.create_rectangle(int(x1),int(y1),int(x2),int(y2),
                                        fill = color_dict["Fuel Bundle"])
                canvas.create_oval(int(x1)+10,int(y1)+10,int(x2)-10,int(y2)-10,
                                   fill = color_dict["Rack"])
                canvas.create_text(int((int(x1)+int(x2))/2),int((int(y1)+int(y2))/2),
                                   text=unit,font=("Verdana", 16))
                bundle_widgets_dict[unit].X = int(x1)
                bundle_widgets_dict[unit].Y = int(y1)

            bundle_widgets_dict[unit].C_c_X = 60
            bundle_widgets_dict[unit].C_c_Y = 60
            for i in range(0,4):
                text = fuel_element_data_dict[unit][i]
                if text in ["CR 1","RR","CR 2","IR"]:
                    Color = color_dict[text]
                else:
                     Color = color_dict["Fuel Element"]
                bundle_widgets_dict[unit].create_oval(fuel_element_coords[i][0],fuel_element_coords[i][1],
                                                          fuel_element_coords[i][2],fuel_element_coords[i][3],
                                                          fill = Color)
                bundle_widgets_dict[unit].create_text(fuel_element_coords[i][4],fuel_element_coords[i][5],
                                                          text=text,font = (8))

        else:
            Color = color_dict[module]
            if module in ["Reflector","Beam Port","Thermal Column","Through Tube","Rabbit","Storage"]:
                canvas.create_rectangle(int(x1),int(y1),
                                            int(x2),int(y2),
                                            fill = Color)
            if module in ["PuBe Source","CIC","FC","IC"]:
                canvas.create_oval(int(x1),int(y1),
                                       int(x2),int(y2),
                                       fill = Color)
            canvas.create_text( (int(x1)+int(x2))/2, (int(y1)+int(y2))/2,
                               text=''.join([module," ",unit]),font = ("Verdana",10,"bold") )

        if module == "Storage":
            bundle_widgets_dict[unit] = tk.Canvas(Core_Canvas,width = 80, height = 80,
                                         bg = color_dict["Storage_Element"],
                                         highlightthickness=0)
            bundle_widgets_dict[unit].X = int(x1)+8
            bundle_widgets_dict[unit].Y = int(y1)+8
            bundle_widgets_dict[unit].C_c_X = 40
            bundle_widgets_dict[unit].C_c_Y = 40

    def Draw_Fuel(unit,state):
        if state.isnumeric() == True:
            bundle_widgets_dict[state].create_text(bundle_widgets_dict[state].C_c_X,
                                                   bundle_widgets_dict[state].C_c_Y,
                                                   text=str(unit),font=("Verdana",10,"bold"))
            bundle_widgets_dict[state].place(x=bundle_widgets_dict[state].X,
                                             y=bundle_widgets_dict[state].Y)
            #Can be easaly generalized by removing if statement
            # FUel bundles placed in storage at the onset and not "new 1-5" get a return button
            if "New" not in unit:
                for i in range(0,len(Buttons)):
                     if (Buttons[i].module == "Return Fuel" and Buttons[i].Key == state):
                        Buttons[i].the_button.place(x=Buttons[i].x1,y=Buttons[i].y1)
                        Button_Hit = i
                        container_dict[state] = [unit,Button_Hit]
        else:
            bundle_widgets_dict[state].place(x=bundle_widgets_dict[state].X,
                                             y=bundle_widgets_dict[state].Y)



# In[7]:


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


# In[8]:


class Controls:
    # canvas = Canvas button's placed on, module = button text, font = font size, Key = location key
    def __init__(self,canvas,module,Init_State,x1,y1,Width,Height,Font,Key):
        self.Key = Key
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.module = module

        #the_command becomes an anonymous function b/c of lambda
        if module == "Select Element":  #for fuel bundles in reactor
            text = "Select"
            the_command = lambda :Controls.Bundle_Selected(Key)
        elif module =="Select Container": #for placing fuel in storage
            text = "Select"
            the_command = lambda :Controls.Container_Selected(Key)
        elif module =="Return Fuel":    #for fuel in storage
            text = "Return"
            the_command = lambda :Controls.Return_Fuel(Key)
        else:
            text = self.module
            the_command = Command_Dict[self.module]

        # make the button
        self.the_button = tk.Button(canvas, bg=color_dict[self.module],
                                 command = the_command,
                                 text=text,font = ("Purisa", Font),
                                 width = Width,
                                 height = Height)
        self.the_button.place(x=self.x1,y=self.y1)
        if Init_State == "Hidden":
            self.the_button.place_forget()

    def SerialConnection_Error():
        messagebox.showinfo("Communication Error",
                            "Serial Connection Lost. Restart this Application and Reconnect.")

    #after clicking "remove fuel"
    def Remove_Fuel():
        #show the buttons with fuel in those places
        for i in range(0,len(Buttons)):
            if (Buttons[i].module == "Select Element"
                and fuel_states[Buttons[i].Key] == Buttons[i].Key):
                Buttons[i].the_button.place(x=Buttons[i].x1,y=Buttons[i].y1)
            #stop showing [return] buttons for fuel in storage
            elif Buttons[i].module == "Return Fuel":
                Buttons[i].the_button.place_forget()

        messagebox.showinfo("Remove Fuel","Select Target Fuel Bundle")

    #after clicking a fuel element in reactor to remove
    def Bundle_Selected(Key):
        global Bundle_Key
        Bundle_Key = Key
        bundle_widgets_dict[Key].place_forget()
        #stop showing all fuel in reactor, show fuel in
        for i in range(0,len(Buttons)):
            if Buttons[i].module == "Select Element":
                Buttons[i].the_button.place_forget()
            #show unfilled storage buttons
            elif (Buttons[i].module == "Select Container" and
                  Buttons[i].Key not in fuel_states.values()):
                Buttons[i].the_button.place(x=Buttons[i].x1,y=Buttons[i].y1)

        messagebox.showinfo("Remove Fuel", "Select Destination")

    #after clicking a storage container to place fuel
    def Container_Selected(Key):
        #makeother buttons disappear & place new button for new fuel in storage
        for i in range(0,len(Buttons)):
            #remove all the "select" buttons
            if Buttons[i].module == "Select Container":
                Buttons[i].the_button.place_forget()
            #put back all the return buttons that have stuff & change fuel state
            elif Buttons[i].module == "Return Fuel":
                #for the fuel that was just placed
                if Buttons[i].Key == Key:
                    Button_Hit = i
                    fuel_states[Bundle_Key] = Key
                #for return buttons
                if Buttons[i].Key in fuel_states.values():
                    Buttons[i].the_button.place(x=Buttons[i].x1,y=Buttons[i].y1)

        bundle_widgets_dict[Key].place(x=bundle_widgets_dict[Key].X,
                                       y=bundle_widgets_dict[Key].Y)
        bundle_widgets_dict[Key].create_text(bundle_widgets_dict[Key].C_c_X,
                                             bundle_widgets_dict[Key].C_c_Y,
                                               text=Bundle_Key,font=("Verdana",10,"bold"))
        container_dict[Key] = [Bundle_Key,Button_Hit]

    #after clicking a fuel in storage
    def Return_Fuel(Key):
        Bundle = container_dict[Key][0]
        fuel_states[Bundle] = Bundle
        Button_Hit = container_dict[Key][1] #different than the bucket number.
                                            #Tagged based off order of creation.
        bundle_widgets_dict[Bundle].place(x=bundle_widgets_dict[Bundle].X,
                                             y=bundle_widgets_dict[Bundle].Y)
        bundle_widgets_dict[Key].place_forget()
        Buttons[Button_Hit].the_button.place_forget()
        del container_dict[Key]

    def Beam_Port_1():
        print("Need BP1")
    def Beam_Port_2():
        print("Need BP2")
    def Rabbit():
        print("Need Rabbit")
    def Through_Tube():
        print("Need TT")


# In[9]: essentially the "main"


master = tk.Tk()
canvas_width = 1920
canvas_height = 1080

master.title("MUTR Status Board")

# Create the canvases
Core_Canvas = tk.Canvas(master,width = 1400,height = canvas_height, bg = 'grey')
Control_Canvas = tk.Canvas(master,width = canvas_width-1400,height=canvas_height, bg = 'grey')

#add all the modules (shapes)
for i in range(1,len(module)):
    Create_Core_Canvas.Draw_Reactor(Core_Canvas,module[i],unit[i],x1[i],y1[i],x2[i],y2[i])

#see if arduino is connected and try giving functionality to the thermal column buttons
Command_Dict = {}

try:
    arduino = Arduino_Control("COM5",3,8,11,3)
    Command_Dict = {"Open Thermal Column":arduino.Open_ThermalColumn,
                    "Close Thermal Column":arduino.Close_ThermalColumn}
except:
    Command_Dict = {"Open Thermal Column":Controls.SerialConnection_Error,
                    "Close Thermal Column":Controls.SerialConnection_Error}
    messagebox.showinfo("Unable to Establish Serial Connection!",
                        "Please verify your device is connected to 'COM5' then restart the Application")


# TODO - Dictionary of commands for buttons - confusing placement
Command_Dict.update({"Remove Fuel":Controls.Remove_Fuel,
                     "Beam Port 1":Controls.Beam_Port_1,
                     "Beam Port 2":Controls.Beam_Port_2,
                     "Rabbit":Controls.Rabbit,
                     "Through Tube":Controls.Through_Tube})

Canvas_Dict = {"Core_Canvas":Core_Canvas,"Control_Canvas":Control_Canvas}

# makes buttons by instantiating i # objects of the Controls class
Buttons = []
for i in range(1,len(Control_Dict)):
    Buttons.append( Controls(Canvas_Dict[Control_Dict[i][0]],Control_Dict[i][1],Control_Dict[i][2],Control_Dict[i][3],
                    Control_Dict[i][4],Control_Dict[i][5],Control_Dict[i][6],Control_Dict[i][7],Control_Dict[i][8]) )

# FIXME this is hard coded and Draw_Fuel is kind of redundant
for i in range(1,25):
    Create_Core_Canvas.Draw_Fuel(unit[i],state[i])

Core_Canvas.grid(row=0,column=0)
Control_Canvas.grid(row=0,column=1)

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

# In[ ]:


#Saving/Exporting Current Fuel Locations for the next startup.
# container_dict
# {Bucket number: [Bundle,return button num]}


# In[ ]:


#We can now use this dict to update the Core_Geometry Spreadsheet!
    #Need to learn how to format outputs so I dont ruin destination file.
print(container_dict)


# In[ ]:





# In[ ]:
