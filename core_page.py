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
        # FIXME: Add stuff here!
        self.ELEMENT_TYPES = frozenset(
            {"Base", "Sample Chamber", "Fuel Storage", "Fuel Bundle", "Sample"})
        self.ELEMENT_COLORS = {"Base": "light gray", "Sample Chamber": "bisque",
                               "Fuel Storage": "bisque", "Fuel Bundle": "azure",
                               "Fuel Rod": "aquamarine", "Control Rod": "pink", "Sample": "light goldenrod",
                               "Green Button": "green yellow", "Red Button": "salmon",
                               "Background": "snow"}

        # Dictionaries that basically hold all the configuration information
        # element_name: grid coords (topleft [0-9][A-Z], bottomright [0-9][A-Z])
        self.element_coordinates = {}
        # element_name: element_type
        self.element_types = {}
        # fuel element_name: fuel element_contains
        self.fuel_bundles = {}
        # sample element_name: sample element_contains
        self.samples = {}

        # Sets also useful for config information
        self.fuel_names = set()
        self.sample_names = set()

        # Set up page properties
        # self.grid_rowconfigure(0, weight=1, minsize=controller.cell_size)
        # self.grid_columnconfigure(0, weight=1, minsize=controller.cell_size)

        self.core_canvas = tk.Canvas(self, height=self.controller.height,
                                     width=self.controller.width*self.controller.NUM_CORE_LENGTH_BLOCKS /
                                     self.controller.NUM_LENGTH_BLOCKS,
                                     bg=self.ELEMENT_COLORS["Background"])
        self.controls_canvas = tk.Canvas(self, height=self.controller.height,
                                         width=self.controller.width*self.controller.NUM_CONTROLS_LENGTH_BLOCKS /
                                         self.controller.NUM_LENGTH_BLOCKS,
                                         bg=self.ELEMENT_COLORS["Background"])

        self.core_canvas.grid(row=0, column=0)
        self.controls_canvas.grid(row=0, column=1)

        # Load core if config exists
        if not self.load_core_configuration():
            controller.destroy()
            controller.popup_message("configuration.csv file not found!")
        elif not self.load_controls_configuration():
            # TODO: IMPLEMENT
            pass

    def draw_page(self):
        # TODO: IMPLEMENT
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

            (topleft_px, bottomright_px) = self.get_pxlocation(topleft_coordinate, bottomright_coordinate)

            if (element_type == "Sample"):
                # TODO: IMPLEMENT
                pass
            else:
                # Draw rectangles
                self.core_canvas.create_rectangle(topleft_px[0], topleft_px[1],
                                                  bottomright_px[0], bottomright_px[1],
                                                  fill=self.ELEMENT_COLORS[element_type])
                # Calculate center pixel used for placing things
                center_px = ((topleft_px[0]+bottomright_px[0])/2, 
                             (topleft_px[1]+bottomright_px[1])/2)

                if (element_type == "Fuel Bundle") and contains:
                    # TODO: Loop somehow?
                    rods = contains.split(",")
                    print(rods)
                    # Top left rod
                    self.core_canvas.create_oval(topleft_px[0],topleft_px[1],
                                                 center_px[0], center_px[1],
                                                 fill=self.ELEMENT_COLORS["Fuel Rod" if rods[0].isnumeric() else "Control Rod"])
                    self.core_canvas.create_text((topleft_px[0]+center_px[0])/2,
                                                 (topleft_px[1]+center_px[1])/2,
                                                 text=rods[0], font=self.controller.SMALL_FONT)
                    # Top right rod
                    self.core_canvas.create_oval(center_px[0],topleft_px[1],
                                                 bottomright_px[0], center_px[1],
                                                 fill=self.ELEMENT_COLORS["Fuel Rod" if rods[1].isnumeric() else "Control Rod"])
                    self.core_canvas.create_text((center_px[0]+bottomright_px[0])/2,
                                                 (topleft_px[1]+center_px[1])/2,
                                                 text=rods[1], font=self.controller.SMALL_FONT)
                    # Bottom left rod
                    self.core_canvas.create_oval(topleft_px[0],center_px[1],
                                                 center_px[0], bottomright_px[1],
                                                 fill=self.ELEMENT_COLORS["Fuel Rod" if rods[2].isnumeric() else "Control Rod"])
                    self.core_canvas.create_text((topleft_px[0]+center_px[0])/2,
                                                 (center_px[1]+bottomright_px[1])/2,
                                                 text=rods[2], font=self.controller.SMALL_FONT)
                    # Bottom right rod
                    self.core_canvas.create_oval(center_px[0],center_px[1],
                                                 bottomright_px[0], bottomright_px[1],
                                                 fill=self.ELEMENT_COLORS["Fuel Rod" if rods[3].isnumeric() else "Control Rod"])
                    self.core_canvas.create_text((center_px[0]+bottomright_px[0])/2,
                                                 (center_px[1]+bottomright_px[1])/2,
                                                 text=rods[3], font=self.controller.SMALL_FONT)
                else:
                    self.core_canvas.create_text(center_px[0], center_px[1],
                                                 text=name, font=self.controller.MEDIUM_FONT)
                # TODO: Account for buttons

            return True

        return False

    def load_core_configuration(self, filename="configuration.csv"):
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

    def load_controls_configuration(self):
        # TODO: IMPLEMENT
        pass

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
