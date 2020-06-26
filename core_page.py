# -*- coding: utf-8 -*-
"""
Start page of the MUTR Status board

Conducted under the Unversity of Maryland
Created on Wed Jun 24 16:34:55 2020
@author: Telon J. Yan
"""
# %% Imports
import tkinter as tk

# %% Start page class
class CorePage(tk.Frame):
    """
    This class, a subclass of tkinter.Frame, creates a tkinder window showing
    the MUTR reactor core configuration and buttons to interact with upon 
    initialization
    """
    
    def __init__(self, parent, controller):
        """
        Overrides tkinter.Frame.__init__() to construct a Frame and populate it
        with the contents of what we want from the core page (window)
        """
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Add objects in start page window
        title_label = tk.Label(self, text="MUTR Core", font=controller.LARGE_FONT)
        title_label.pack(side="top", fill="x", pady=10)
        
        button1 = tk.Button(self, text="Go to Test Page", font=controller.SMALL_FONT, 
                            command=lambda: controller.show_frame("TestPage"))
        button1.pack()