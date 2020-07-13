# -*- coding: utf-8 -*-
"""
Start page of the MUTR Status board

Conducted under the Unversity of Maryland
Created on Wed Jun 24 16:34:55 2020
@author: Telon J. Yan
"""
# %% Imports
import tkinter as tk
import csv
import re

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

        An instance of this' parent is the Frame instance in status_board.py 
        and its controller is the StatusBoard(tk.Tk)
        """
        ## Inheritance
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        ## Variables in this reactor core page instance
        # Constant variables
        self.ELEMENT_TYPES = frozenset({"Base", "Sample Chamber", "Fuel Bundle", "Fuel Storage"})

        # These dictionaries are dumb rn - think about how you want to structure this
        self.fuel_locations = {}
        self.sample_chambers = {}
        self.fuel_storages = {}


        # Set up page properties (grid)
        self.grid_rowconfigure(0, weight=1, minsize=controller.cell_size)
        self.grid_columnconfigure(0, weight=1, minsize=controller.cell_size)
        
        # Load core if config exists
        if not self.load_configuration():
            controller.destroy()
            controller.popup_message("configuration.csv file not found!")
        else:
            # Add objects in start page window
            title_label = tk.Label(self, text="MUTR Core", font=controller.LARGE_FONT)
            title_label.pack(side="top", fill="x", pady=10)
            
            button1 = tk.Button(self, text="Go to Test Page", font=controller.SMALL_FONT, 
                                command=lambda: controller.show_frame("TestPage"))
            button1.pack()

    def draw_page(self):
        pass

    def draw_element(self, element_type, name, topleft_px, bottomright_px, contains=None):
        """
        Draws an element specified by method parameters

        Parameters:
            element_type (String): The type of element. Must be in self.ELEMENT_TYPES
            name (String): Name of the element, usually used to label it
            topleft_px (tuple): (x,y) tuple of the element's top left px position
            bottomright_px (tuple): (x,y) tuple of the element's bottom right px position
            contains (String): Stuff contained in this element. See configuration.csv for details

        Returns:
            True (boolean) if the element was successfully drawn, False otherwise
        """
        if (element_type in self.ELEMENT_TYPES) and name and topleft_px and bottomright_px:
            try:
                if (element_type == "Base"):
                    pass
                elif (element_type == "Sample Chamber"):
                    pass
                elif (element_type == "Fuel Bundle"):
                    pass
                elif (element_type == "Fuel Storage"):
                    pass
                
                return True
            except:
                pass
        
        return False

    def load_configuration(self, filename="configuration.csv"):
        """
        Parses a .csv file of a reactor core's configuration and
        loads the element data into self.
        
        Parameters:
            filename (String): The filename of the csv core configuration file.
                This defaults to configuration.csv if not specified by user.

        Returns:
            True (boolean) if the loading was successful, False otherwise
        """
        try:
            with open(filename, encoding='utf-8-sig') as core_configuration_data:
                core_reader = csv.DictReader(core_configuration_data, delimiter=',')
                
                # Per row of csv, add stuff
                for row in core_reader:
                    #print(row)
                    #print(row["Type of Element"], row["Name"], row["Top Left Coordinate"], row["Bottom Right Coordinate"], row["Contains"])

                    # Calculate pixel coordinate location
                    # coord_tuple[0][0] = TL x, coord_tuple[0][1] = TL y, coord_tuple[1][0] = BR x, coord_tuple[1][1] = BR y
                    coord_tuple = self.get_pxlocation(row["Top Left Coordinate"], row["Bottom Right Coordinate"])
                    
                    # Add element to self variables

                    # Draw element
                    self.draw_element(row["Type of Element"], row["Name"], coord_tuple[0], coord_tuple[1], row["Contains"])

            return True
        
        except OSError:
            return False

    def get_pxlocation(self, topleft, bottomright):
        """
        Given two [0-9][A-Z] format coordinates (row-column as in configuration.csv)
        and properties of the Frame, returns pixel (int) coordinates corresponding
        to them. Assumes the [0-9][A-Z] grid has no more than 26 columns (does not
        support multiple alphanumeric letters)

        Parameters:
            topleft (String): the top left coordinate in [0-9][A-Z] format of some
                rectanglar area as in configuration.csv
            bottomright (String): the bottom right coordinate of said rectangular area

        Returns:
            Tuple of two length-2 tuples: the topleft and bottomright coordinates of the corners
            of the rectangle in pixels instead of [0-9][A-Z]
        """
        # The configuration file coordinates are in row x column format, so
        # topleft_split and bottomright_split are (y, x) right now
        topleft_split = re.compile("([0-9]+)([a-zA-Z]+)").match(topleft).groups()
        bottomright_split = re.compile("([0-9]+)([a-zA-Z]+)").match(bottomright).groups()
        
        topleft_tuple = ((ord(topleft_split[1].lower())-96-1)*self.controller.cell_size, 
                        (int(topleft_split[0])-1)*self.controller.cell_size)
        bottomright_tuple = ((ord(bottomright_split[1].lower())-96)*self.controller.cell_size, 
                            int(bottomright_split[0])*self.controller.cell_size)

        return (topleft_tuple, bottomright_tuple)