# -*- coding: utf-8 -*-
"""
An interactive status board for the Maryland University Training Reactor (MUTR)

Tries to follow standard code style: https://www.python.org/dev/peps/pep-0008

Created on Tue Jun 23 10:57:39 2020
@author: Telon J. Yan
"""
# %% Imports
import tkinter as tk

#Import user-defined pages
import start_page
import test_page


# %% Main Tkinter class
class StatusBoard(tk.Tk):
    
    #Initialize status board window
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #Define the fonts we want to use
        self.LARGE_FONT = ("Verdana", 12)
        self.MEDIUM_FONT = ("Verdana", 10)
        self.SMALL_FONT = ("Verdana", 8)
        
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Dictionary of string frame names to Frame instances
        self.frames = {}
        #Populate self.frames
        for F in (start_page.StartPage, test_page.TestPage):
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

# %% Execute Code
if __name__ == "__main__":
    master = StatusBoard()
    master.mainloop()