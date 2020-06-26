# -*- coding: utf-8 -*-
"""
An interactive status board for the Maryland University Training Reactor (MUTR)
This file

Tries to follow standard code style: https://www.python.org/dev/peps/pep-0008

Conducted under the Unversity of Maryland
Created on Thu Jun 25 14:45:17 2020
@author: Telon J. Yan
"""

# %% Imports
import tkinter as tk
# Import user-defined pages
from core_page import CorePage
from test_page import TestPage

# %% Main Tkinter class
class StatusBoard(tk.Tk):
    """
    Instances of this class are fully functional TKinter Status Board windows

    Attributes:
        LARGE_FONT (tuple): Large tuple font for Tkinter use (Helvetica bold size 12)
        MEDIUM_FONT (tuple): Medium sized tuple font for Tkinter use (Helvetica size 10)
        SMALL_FONT (tuple): Small font for Tkinter use (Helvetica size 8)
        frames (String:tkinter.Frame dictionary): Dictionary of page names to their instances (a Frame)

    Methods:
        show_frame(page_name):
            Changes the window to show the page associated with page_name
        popup_message(message):
            Creates and displays a simple pop up message containing the message parameter
    """

    # %% Initialize status board window
    def __init__(self, *args, **kwargs):
        """
        Overrides tkinter.Tk.__init__() to build a tkinter screen with the
        desired attributes of the Status Board window and toolbar. 
        """
        
        tk.Tk.__init__(self, *args, **kwargs)

        # Define attributes
        # The fonts we want to use
        self.LARGE_FONT = ("Helvetica", 12, "bold")
        self.MEDIUM_FONT = ("Helvetica", 10)
        self.SMALL_FONT = ("Helvetica", 8)
        # Dictionary of string frame names to Frame instances
        self.frames = {}

        ## Set up menubar
        menubar = tk.Menu(self)
        # File submenu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Configuration", command=lambda: self.popup_message("Not yet supported"))
        filemenu.add_command(label="Load Configuration", command=lambda: self.popup_message("Not yet supported"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)
        # Add elements to bar
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label="Options", command=lambda: self.popup_message("Not yet supported"))
        menubar.add_command(label="Help", command=lambda: self.popup_message("Not yet supported"))

        self.config(menu=menubar)

        # Set up initial window and attributes
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Populate self.frames
        for F in (CorePage, TestPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Frames all at same place --> move btwn them by raising in stack
            frame.grid(row=0, column=0, sticky="nsew")

        # Icon must be a .ico
        # tk.Tk.iconbitmap(self, default="DEFAULT.ico")
        self.title("MUTR Status Board")
        # Start up the program on the core page
        self.show_frame("CorePage")

    # %% show_frame method
    def show_frame(self, page_name):
        """
        Displays the page (frame) associated with parameter page_name

        Parameters:
            page_name (String): The name associated with a page, also the name 
            of the class that page belongs to (e.g. "CorePage")
            
        Returns:
            None
        """
        frame = self.frames[page_name]
        frame.tkraise()

    # %% popup_message method
    def popup_message(self, message):
        """
        Creates and displays a simple pop up message containing the message parameter

        Parameters:
            message (String): The message to be displayed in the pop-up window
            
        Returns:
            None
        """
        popup = tk.Tk()
        popup.title("Note")

        label = tk.Label(popup, text=message)
        okaybutton = tk.Button(popup, text="Okay", font=self.SMALL_FONT,
                               command=lambda:popup.destroy())

        label.pack()
        okaybutton.pack()

        popup.mainloop()
