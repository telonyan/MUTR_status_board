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
        # width, height, and cell size to be calculated with self.__determine_window_size()
        self.width = 0
        self.height = 0
        self.cell_size = 0
        # The fonts we want to use
        self.LARGE_FONT = ("Helvetica", 12, "bold")
        self.MEDIUM_FONT = ("Helvetica", 10)
        self.SMALL_FONT = ("Helvetica", 8)
        # Dictionary of string frame names to Frame instances
        self.frames = {}
        # "Private" variables
        self._NUM_LENGTH_BLOCKS = 26
        self._NUM_HEIGHT_BLOCKS = 19

        # Set up initial window and window properties
        # Determine desired width, height, and cell size of window
        if not self.__determine_window_size():
            self.popup_message("Your screen is not large enough to display this!")
        # Set desired width & height of window
        self.geometry(str(self.width) + "x" + str(self.height))

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

        # Set up menubar
        menubar = tk.Menu(self)
        # File submenu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Configuration",
                             command=lambda: self.popup_message("Not yet supported"))
        filemenu.add_command(label="Load Configuration",
                             command=lambda: self.popup_message("Not yet supported"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)
        # Add elements to bar
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label="Options", command=lambda: self.popup_message("Not yet supported"))
        menubar.add_command(label="Help", command=lambda: self.popup_message("Not yet supported"))

        self.config(menu=menubar)

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
                               command=lambda: popup.destroy())

        label.pack()
        okaybutton.pack()

        popup.mainloop()

    # %% determine_window_size method
    def __determine_window_size(self):
        """
        Private method that sets self.width, self.height, and self.cell_size to 
        appropriate values given the size of the computer screen being used and 
        desired tkinter window ratio specified by private variables (unnecessary
        to be seen).

        Parameters:
            None

        Returns
            True if succeeded, False if the screen fails to be suitable for display.
            If failed, no assignment takes place.
        """
        # -100 is to account for the typical size of taskbars and a little extra room
        screen_height = self.winfo_screenheight() - 100
        screen_width = self.winfo_screenwidth()

        if (screen_height > 0) and (screen_width > 0):

            if (float(screen_height) / screen_width) > (float(self._NUM_HEIGHT_BLOCKS) / self._NUM_LENGTH_BLOCKS):
                # Highest px # of an exact multiple of the # lengthwise blocks we want
                self.cell_size = screen_width // self._NUM_LENGTH_BLOCKS
                self.width = self.cell_size * self._NUM_LENGTH_BLOCKS
                self.height = self.width * self._NUM_HEIGHT_BLOCKS // self._NUM_LENGTH_BLOCKS
            else:
                # Highest px # of an exact multiple of the # heightwise blocks we want
                self.cell_size = screen_height // self._NUM_HEIGHT_BLOCKS
                self.height = self.cell_size * self._NUM_HEIGHT_BLOCKS
                self.width = self.height * self._NUM_LENGTH_BLOCKS // self._NUM_HEIGHT_BLOCKS

            #print(str(self.width) + ", " + str(self.height) + ", " + str(self.cell_size))
            return True

        else:
            return False
