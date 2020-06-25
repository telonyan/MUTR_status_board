# -*- coding: utf-8 -*-
"""
An interactive status board for the Maryland University Training Reactor (MUTR)

Tries to follow standard code style: https://www.python.org/dev/peps/pep-0008

Conducted under the Unversity of Maryland
Created on Thu Jun 25 14:45:17 2020
@author: Telon J. Yan
"""

# %% Imports
import tkinter as tk
from tkinter import ttk

#Import user-defined pages
from start_page import StartPage
from test_page import TestPage

# %% Main Tkinter class
class StatusBoard(tk.Tk):
    
    #Initialize status board window
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #Define variables
        #The fonts we want to use
        self.LARGE_FONT = ("Helvetica", 12, "bold")
        self.MEDIUM_FONT = ("Helvetica", 10)
        self.SMALL_FONT = ("Helvetica", 8)
        #Dictionary of string frame names to Frame instances
        self.frames = {}
        
        #icon must be a .ico
        #tk.Tk.iconbitmap(self, default=".ico")
        tk.Tk.wm_title(self, "MUTR Status Board")
        
        #Set up window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Define the menubar
        menubar = tk.Menu(container)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Configuration", command=lambda: self.popupmsg("Not yet supported"))
        filemenu.add_command(label="Load Configuration", command=lambda: self.popupmsg("Not yet supported"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)
        
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label="Options", command=lambda: self.popupmsg("Not yet supported"))
        menubar.add_command(label="Help", command=lambda: self.popupmsg("Not yet supported"))
        
        tk.Tk.config(self, menu=menubar)
        
        #Populate self.frames
        for F in (StartPage, TestPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            
            # Frames all at same place --> move btwn them by raising in stack
            frame.grid(row=0, column=0, sticky="nsew")
        
        #Start up the program on the start page
        self.show_frame("StartPage")
        
    # Show page (frame) associated with page_name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()        
        
    def popupmsg(self, msg):
        popup = tk.Tk()
        
        popup.wm_title("")
        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        
        button1 = ttk.Button(popup, text="Okay", command=lambda:popup.destroy())
        button1.pack()
        
        popup.mainloop()