#!/usr/bin/env python
# coding: utf-8
"""
Future Improvements:
    -Create a a spreadsheet to record experimentl data.
    -Need to create popup to ask for data. 
    -Need to create method to store data in spreadsheet.1)Experimental Ports:
    -Display/Document experiments
    -Ex: rabbit in core, experiment in beam port2)Fuel Movement:
    -Suppress buttons for invalid operations from displaying 
"""
# In[1]: imports


from tkinter import *
from tkinter import messagebox #messagebox is a module, not a class
import csv
import pyfirmata
import time

# In[2]: Initializing variables


Color_Dict ={"Fuel Bundle":'#3F3B35', "Fuel Element":'#1E3A95',
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


#Importing FuelElement_Data
FuelElement_Data_Dict = {}
with open('fuel_elements.csv', encoding='utf-8-sig') as FuelElement_Data:
    read_FuelElement_Data = csv.reader(FuelElement_Data, delimiter=',')
    for row in read_FuelElement_Data:
        FuelElement_Data_Dict[row[0]] = [ row[1],row[2],row[3],row[4] ]

Element_Coord = {0:[57,57,1,1,29,29],
                 1:[61,57,117,1,89,29],
                 2:[57,61,1,117,29,89],
                 3:[61,61,117,117,89,89]}


# In[4]: Initializing variables related to core geometry


#Importing Core Geometry
Module = []
Unit = []
X1 = []
Y1 = []
X2 = []
Y2 = []
State = []
fuel_states = {}

with open('core_geometry.csv', encoding='utf-8-sig') as CoreGeometry_Data:
    read_CoreGeometry_Data = csv.reader(CoreGeometry_Data, delimiter=',')
    for row in read_CoreGeometry_Data:
        Module.append(row[0])
        Unit.append(row[1])
        X1.append(row[2])
        Y1.append(row[3])
        X2.append(row[4])
        Y2.append(row[5])
        State.append(row[6])
        
        # Dictionary of fuel bundles mapped to where they are
        if row[6]:
            fuel_states[row[1]] = row[6]
        
Bundle_Widgets_Dict = {}
Container_Dict = {}


# In[5]: initializing variables related to control widgets


#Importing dictionary of buttons
Control_Dict = {}
with open('control_widgets.csv', encoding='utf-8-sig') as ControlWidget_Data:
    read_ControlWidget_Data = csv.reader(ControlWidget_Data, delimiter=',')
    for row in read_ControlWidget_Data:
        Control_Dict[int(row[0])] = [ row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]  ] 


# In[6]:


class Create_Core_Canvas: #would like to update name    
    def Draw_Reactor(canvas,Module,Unit,X1,Y1,X2,Y2):
        if Module == "Fuel Bundle":
            Bundle_Widgets_Dict[Unit] = Canvas(Core_Canvas,width = 118, height = 118,
                                                   bg = Color_Dict["Fuel Bundle"],
                                                   highlightthickness=0)
            #Once we have a location for the new fuel, this can be easily generalized
            #by simply removing the if statment.
            if "New" not in Unit:
                canvas.create_rectangle(int(X1),int(Y1),int(X2),int(Y2),
                                        fill = Color_Dict["Fuel Bundle"])
                canvas.create_oval(int(X1)+10,int(Y1)+10,int(X2)-10,int(Y2)-10,
                                   fill = Color_Dict["Rack"])
                canvas.create_text(int((int(X1)+int(X2))/2),int((int(Y1)+int(Y2))/2),
                                   text=Unit,font=("Verdana", 16))
                Bundle_Widgets_Dict[Unit].X = int(X1)
                Bundle_Widgets_Dict[Unit].Y = int(Y1)
            
            Bundle_Widgets_Dict[Unit].C_c_X = 60
            Bundle_Widgets_Dict[Unit].C_c_Y = 60
            for i in range(0,4):
                text = FuelElement_Data_Dict[Unit][i]
                if text in ["CR 1","RR","CR 2","IR"]:
                    Color = Color_Dict[text]
                else:
                     Color = Color_Dict["Fuel Element"]
                Bundle_Widgets_Dict[Unit].create_oval(Element_Coord[i][0],Element_Coord[i][1],
                                                          Element_Coord[i][2],Element_Coord[i][3],
                                                          fill = Color)
                Bundle_Widgets_Dict[Unit].create_text(Element_Coord[i][4],Element_Coord[i][5],
                                                          text=text,font = (8))
                       
        else:
            Color = Color_Dict[Module]
            if Module in ["Reflector","Beam Port","Thermal Column","Through Tube","Rabbit","Storage"]:
                canvas.create_rectangle(int(X1),int(Y1),
                                            int(X2),int(Y2),
                                            fill = Color)
            if Module in ["PuBe Source","CIC","FC","IC"]:
                canvas.create_oval(int(X1),int(Y1),
                                       int(X2),int(Y2),
                                       fill = Color)
            canvas.create_text( (int(X1)+int(X2))/2, (int(Y1)+int(Y2))/2,
                               text=''.join([Module," ",Unit]),font = ("Verdana",10,"bold") )    
        
        if Module == "Storage":
            Bundle_Widgets_Dict[Unit] = Canvas(Core_Canvas,width = 80, height = 80,
                                         bg = Color_Dict["Storage_Element"],
                                         highlightthickness=0)
            Bundle_Widgets_Dict[Unit].X = int(X1)+8
            Bundle_Widgets_Dict[Unit].Y = int(Y1)+8
            Bundle_Widgets_Dict[Unit].C_c_X = 40
            Bundle_Widgets_Dict[Unit].C_c_Y = 40
            
    def Draw_Fuel(Unit,State):                
        if State.isnumeric() == True:
            Bundle_Widgets_Dict[State].create_text(Bundle_Widgets_Dict[State].C_c_X,
                                                   Bundle_Widgets_Dict[State].C_c_Y,
                                                   text=str(Unit),font=("Verdana",10,"bold"))
            Bundle_Widgets_Dict[State].place(x=Bundle_Widgets_Dict[State].X,
                                             y=Bundle_Widgets_Dict[State].Y)  
            #Can be easaly generalized by removing if statement
            # FUel bundles placed in storage at the onset and not "new 1-5" get a return button
            if "New" not in Unit:
                for i in range(0,len(Buttons)):
                     if (Buttons[i].Module == "Return Fuel" and Buttons[i].Key == State):
                        Buttons[i].the_button.place(x=Buttons[i].X1,y=Buttons[i].Y1)
                        Button_Hit = i
                        Container_Dict[State] = [Unit,Button_Hit]
        else:
            Bundle_Widgets_Dict[State].place(x=Bundle_Widgets_Dict[State].X,
                                             y=Bundle_Widgets_Dict[State].Y)
                


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
    # canvas = Canvas button's placed on, Module = button text, font = font size, Key = location key
    def __init__(self,canvas,Module,Init_State,X1,Y1,Width,Height,Font,Key):
        self.Key = Key
        self.X1 = int(X1)
        self.Y1 = int(Y1)
        self.Module = Module
        
        #the_command becomes an anonymous function b/c of lambda
        if Module == "Select Element":  #for fuel bundles in reactor
            text = "Select"
            the_command = lambda :Controls.Bundle_Selected(Key)
        elif Module =="Select Container": #for placing fuel in storage
            text = "Select"
            the_command = lambda :Controls.Container_Selected(Key)
        elif Module =="Return Fuel":    #for fuel in storage
            text = "Return"
            the_command = lambda :Controls.Return_Fuel(Key)
        else:
            text = self.Module
            the_command = Command_Dict[self.Module]
            
        # make the button
        self.the_button = Button(canvas, bg=Color_Dict[self.Module], 
                                 command = the_command,
                                 text=text,font = ("Purisa", Font),  
                                 width = Width, 
                                 height = Height)    
        self.the_button.place(x=self.X1,y=self.Y1)
        if Init_State == "Hidden":
            self.the_button.place_forget()
        
    def SerialConnection_Error():
        messagebox.showinfo("Communication Error",
                            "Serial Connection Lost. Restart this Application and Reconnect.")
        
    #after clicking "remove fuel"
    def Remove_Fuel():
        #show the buttons with fuel in those places
        for i in range(0,len(Buttons)):
            if (Buttons[i].Module == "Select Element" 
                and fuel_states[Buttons[i].Key] == Buttons[i].Key):
                Buttons[i].the_button.place(x=Buttons[i].X1,y=Buttons[i].Y1)
            #stop showing [return] buttons for fuel in storage
            elif Buttons[i].Module == "Return Fuel":
                Buttons[i].the_button.place_forget()
                
        messagebox.showinfo("Remove Fuel","Select Target Fuel Bundle")
        
    #after clicking a fuel element in reactor to remove
    def Bundle_Selected(Key):
        global Bundle_Key
        Bundle_Key = Key
        Bundle_Widgets_Dict[Key].place_forget()
        #stop showing all fuel in reactor, show fuel in 
        for i in range(0,len(Buttons)):
            if Buttons[i].Module == "Select Element":
                Buttons[i].the_button.place_forget()
            #show unfilled storage buttons
            elif (Buttons[i].Module == "Select Container" and 
                  Buttons[i].Key not in fuel_states.values()):
                Buttons[i].the_button.place(x=Buttons[i].X1,y=Buttons[i].Y1)

        messagebox.showinfo("Remove Fuel", "Select Destination")
    
    #after clicking a storage container to place fuel
    def Container_Selected(Key):
        #makeother buttons disappear & place new button for new fuel in storage
        for i in range(0,len(Buttons)):
            #remove all the "select" buttons
            if Buttons[i].Module == "Select Container":
                Buttons[i].the_button.place_forget()
            #put back all the return buttons that have stuff & change fuel state
            elif Buttons[i].Module == "Return Fuel":
                #for the fuel that was just placed
                if Buttons[i].Key == Key:
                    Button_Hit = i
                    fuel_states[Bundle_Key] = Key
                #for return buttons
                if Buttons[i].Key in fuel_states.values():
                    Buttons[i].the_button.place(x=Buttons[i].X1,y=Buttons[i].Y1)
                    
        Bundle_Widgets_Dict[Key].place(x=Bundle_Widgets_Dict[Key].X,
                                       y=Bundle_Widgets_Dict[Key].Y)
        Bundle_Widgets_Dict[Key].create_text(Bundle_Widgets_Dict[Key].C_c_X,
                                             Bundle_Widgets_Dict[Key].C_c_Y,
                                               text=Bundle_Key,font=("Verdana",10,"bold"))
        Container_Dict[Key] = [Bundle_Key,Button_Hit]

    #after clicking a fuel in storage
    def Return_Fuel(Key):
        Bundle = Container_Dict[Key][0]
        fuel_states[Bundle] = Bundle
        Button_Hit = Container_Dict[Key][1] #different than the bucket number.
                                            #Tagged based off order of creation.
        Bundle_Widgets_Dict[Bundle].place(x=Bundle_Widgets_Dict[Bundle].X,
                                             y=Bundle_Widgets_Dict[Bundle].Y)
        Bundle_Widgets_Dict[Key].place_forget()
        Buttons[Button_Hit].the_button.place_forget()
        del Container_Dict[Key]

    def Beam_Port_1():
        print("Need BP1")
    def Beam_Port_2():
        print("Need BP2")
    def Rabbit():
        print("Need Rabbit")
    def Through_Tube():
        print("Need TT")


# In[9]: essentially the "main"


master = Tk()
canvas_width = 1920
canvas_height = 1080  

master.title("MUTR Status Board")

# Create the canvases
Core_Canvas = Canvas(master,width = 1400,height = canvas_height, bg = 'grey')
Control_Canvas = Canvas(master,width = canvas_width-1400,height=canvas_height, bg = 'grey')

#add all the modules (shapes)
for i in range(1,len(Module)):
    Create_Core_Canvas.Draw_Reactor(Core_Canvas,Module[i],Unit[i],X1[i],Y1[i],X2[i],Y2[i])

#see if arduino is connected and try giving functionality to the thermal column buttons
try:
    Hardware = Arduino_Control("COM5",3,8,11,3)
    Command_Dict = {"Open Thermal Column":Hardware.Open_ThermalColumn,
                    "Close Thermal Column":Hardware.Close_ThermalColumn}
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
    Create_Core_Canvas.Draw_Fuel(Unit[i],State[i])        
    
Core_Canvas.grid(row=0,column=0)
Control_Canvas.grid(row=0,column=1)

master.update_idletasks()  
master.update()  
master.mainloop()


# In[10]: Close arduino connection


#Ensuring the shutter is closed sfter closing the application
try:
    Hardware.Open_Light.write(0)
    Hardware.Shutter_Motor.write(0)
    Hardware.Servo.write(0)
    time.sleep(1.5)
    Hardware.board.exit()
except:
    messagebox.showinfo("Serial Connection Error","The serial connection was lost prior to closing the application\nPlease verify the shutter is closed.")


# In[ ]:


#Saving/Exporting Current Fuel Locations for the next startup.
# Container_Dict
# {Bucket number: [Bundle,return button num]}


# In[ ]:


#We can now use this dict to update the Core_Geometry Spreadsheet!
    #Need to learn how to format outputs so I dont ruin destination file.
print(Container_Dict)   


# In[ ]:





# In[ ]:




