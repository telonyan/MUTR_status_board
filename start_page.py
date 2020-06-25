# -*- coding: utf-8 -*-
"""
Start page of the MUTR Status board

Created on Wed Jun 24 16:34:55 2020
@author: Telon J. Yan
"""
# %% Imports
import tkinter as tk
from tkinter import ttk

# %% Start page class
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Add objects in start page window
        title_label = tk.Label(self, text="MUTR Core", font=controller.LARGE_FONT)
        title_label.pack(side="top", fill="x", pady=10)
        
        button1 = tk.Button(self, text="Go to Test Page", font=controller.SMALL_FONT, 
                            command=lambda: controller.show_frame("TestPage"))
        button1.pack()