# -*- coding: utf-8 -*-
"""
An interactive status board for the Maryland University Training Reactor (MUTR)

Tries to follow standard code style: https://www.python.org/dev/peps/pep-0008

Created on Tue Jun 23 10:57:39 2020
@author: Telon Yan
"""
# %% Imports
import tkinter as tk

#Import other user-defined pages


# %% Defining constants
LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


# %% Main Tkinter class
class StatusBoard(tk.Tk):
    
    #Initialize status board window
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Dictionary of string frame names to Frame instances
        self.frames = {}
            
        #Populate self.frames
        for F in (StartPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            
            # Frames all at same place --> move btwn them by raising in stack
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")
        
    # Show page (frame) associated with page_name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
# %% Start page class
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #Add objects in start page window
        
        

# %% Executor
masterApp = StatusBoard()
masterApp.mainloop()