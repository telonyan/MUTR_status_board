#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 19:00:44 2020

@author: tydar
"""


from tkinter import *
from tkinter import messagebox

class Controls:
    def __init__(self,canvas,Module,Init_State,X1,Y1,Width,Height,Font,Key):
        self.Key = Key
        self.X1 = int(X1)
        self.Y1 = int(Y1)
        self.Module = Module
        if Module == "Select Element":
            text = "Select"
            the_command = lambda :Controls.Bundle_Selected(Key)
        elif Module =="Select Container":
            text = "Select"
            the_command = lambda :Controls.Container_Selected(Key)
        elif Module =="Return Fuel":
            text = "Return"
            the_command = lambda :Controls.Return_Fuel(Key)
        else:
            text = self.Module
            the_command = Command_Dict[self.Module]
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
        
    def Remove_Fuel():
        for i in range(0,len(Buttons)):
            if Buttons[i].Module == "Select Element":
                Buttons[i].the_button.place(x=Buttons[i].X1,y=Buttons[i].Y1)
        messagebox.showinfo("Remove Fuel","Select Target Fuel Bundle")
        
    def Bundle_Selected(Key):
        global Bundle_Key
        Bundle_Key = Key
        Bundle_Widgets_Dict[Key].place_forget()
        for i in range(0,len(Buttons)):
            if Buttons[i].Module == "Select Element":
                Buttons[i].the_button.place_forget()
            if Buttons[i].Module == "Select Container":
                Buttons[i].the_button.place(x=Buttons[i].X1,y=Buttons[i].Y1)
        messagebox.showinfo("Remove Fuel", "Select Destination")
    
    def Container_Selected(Key):
        for i in range(0,len(Buttons)):
                if Buttons[i].Module == "Select Container":
                    Buttons[i].the_button.place_forget()
                if (Buttons[i].Module == "Return Fuel" and Buttons[i].Key == Key):
                    Buttons[i].the_button.place(x=Buttons[i].X1,y=Buttons[i].Y1)
                    Button_Hit = i
        Bundle_Widgets_Dict[Key].place(x=Bundle_Widgets_Dict[Key].X,
                                       y=Bundle_Widgets_Dict[Key].Y)
        Bundle_Widgets_Dict[Key].create_text(Bundle_Widgets_Dict[Key].C_c_X,
                                             Bundle_Widgets_Dict[Key].C_c_Y,
                                               text=Bundle_Key,font=("Verdana",10,"bold"))
        Container_Dict[Key] = [Bundle_Key,Button_Hit]

    def Return_Fuel(Key):
        Bundle = Container_Dict[Key][0]
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