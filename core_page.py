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
        # Inheritance
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Variables in this reactor core page instance
        # Constant variables
        self.ELEMENT_TYPES = frozenset(
            {"Base", "Sample Chamber", "Fuel Storage", "Fuel Bundle", "Sample"})
        self.ELEMENT_COLORS = {"Base": "gray", "Sample Chamber": "khaki",
                               "Fuel Storage": "khaki", "Fuel Bundle": "azure",
                               "Fuel Element": "aquamarine", "Sample": "light goldenrod",
                               "Green Button": "green yellow", "Red Button": "salmon",
                               "Background": "snow"}

        # Dictionaries that basically hold all the configuration information
        # element_name : grid coords (topleft [0-9][A-Z], bottomright [0-9][A-Z])
        self.element_coordinates = {}
        # element_name : element_type
        self.element_types = {}
        # fuel element_name : fuel element_contains
        self.fuel_bundles = {}
        # sample element_name : sample element_contains
        self.samples = {}

        # Sets also useful for config information
        self.fuel_names = set()
        self.sample_names = set()

        # Set up page properties
        # self.grid_rowconfigure(0, weight=1, minsize=controller.cell_size)
        # self.grid_columnconfigure(0, weight=1, minsize=controller.cell_size)

        self.core_canvas = tk.Canvas(self, height=self.controller.height,
                                     width=self.controller.width*22/26, bg=self.ELEMENT_COLORS["Background"])
        self.control_canvas = tk.Canvas(self, height=self.controller.height,
                                        width=self.controller.width*4/26, bg=self.ELEMENT_COLORS["Background"])

        self.core_canvas.grid(row=0, column=0)
        self.control_canvas.grid(row=0, column=1)

        # Load core if config exists
        if not self.load_configuration():
            controller.destroy()
            controller.popup_message("configuration.csv file not found!")
        else:
            # Add objects in start page window
            pass

            # title_label = tk.Label(self, text="MUTR Core", font=controller.LARGE_FONT)
            # title_label.pack(side="top", fill="x", pady=10)

            # button1 = tk.Button(self, text="Go to Test Page", font=controller.SMALL_FONT,
            #                     command=lambda: controller.show_frame("TestPage"))
            # button1.pack()

    def draw_page(self):
        pass

    def draw_element(self, element_type, name, topleft_coordinate, bottomright_coordinate, contains=None):
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
        if (element_type in self.ELEMENT_TYPES) and name and topleft_coordinate and bottomright_coordinate:

            (topleft_px, bottomright_px) = self.get_pxlocation(
                topleft_coordinate, bottomright_coordinate)

            if (element_type == "Base"):
                pass
            elif (element_type == "Sample Chamber"):
                pass
            elif (element_type == "Fuel Storage"):
                pass
            elif (element_type == "Fuel Bundle"):
                pass
            elif (element_type == "Sample"):
                pass

            return True

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
                core_reader = csv.DictReader(core_configuration_data)

                # Per row of csv, add stuff
                for row in core_reader:
                    # Set read values to temporary variables
                    temp_type = row["Type of Element"]
                    temp_name = row["Name"]
                    temp_topleft = row["Top Left Coordinate"]
                    temp_bottomright = row["Bottom Right Coordinate"]
                    temp_contains = row["Contains"]

                    if (temp_type in self.ELEMENT_TYPES):
                        # Update CorePage variables (dictionaries)
                        self.element_types[temp_name] = temp_type
                        self.element_coordinates[temp_name] = (temp_topleft, temp_bottomright)

                        if (temp_type == "Fuel Bundle"):
                            self.fuel_names.add(temp_name)
                            self.fuel_bundles[temp_name] = temp_contains
                        elif (temp_type == "Sample"):
                            self.sample_names.add(temp_name)
                            self.samples[temp_name] = temp_contains

                        # Draw element
                        if not self.draw_element(temp_type, temp_name, temp_topleft, temp_bottomright, temp_contains):
                            print("Element could not be drawn")
                            raise ValueError

                    else:
                        print("Invalid element type")
                        raise ValueError

            return True

        except csv.Error as e:
            print(e)
            return False
        except ValueError as e:
            print(e)
            return False

    def get_pxlocation(self, topleft_coordinate, bottomright_coordinate):
        """
        Given two row [0-9] x column [A-Z] format coordinates (as in configuration.csv)
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
        # topleft_split and bottomright_split become (y, x)
        topleft_split = re.compile(
            "([0-9]+)([a-zA-Z]+)").match(topleft_coordinate).groups()
        bottomright_split = re.compile(
            "([0-9]+)([a-zA-Z]+)").match(bottomright_coordinate).groups()

        topleft_px = ((ord(topleft_split[1].lower())-96-1)*self.controller.cell_size,
                      (int(topleft_split[0])-1)*self.controller.cell_size)
        bottomright_px = ((ord(bottomright_split[1].lower())-96)*self.controller.cell_size,
                          int(bottomright_split[0])*self.controller.cell_size)

        return (topleft_px, bottomright_px)
