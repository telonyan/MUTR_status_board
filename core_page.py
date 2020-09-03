# -*- coding: utf-8 -*-
"""
Start page of the MUTR Status board

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""
# %% Imports
import tkinter as tk
import csv
import re
import board_state
from element_control_button import ElementControlButton
from element_fuel_bundle import ElementFuelBundle
from element_fuel_storage import ElementFuelStorage
from element_sample import ElementSample
from element_sample_chamber import ElementSampleChamber
from element_noninteractable import ElementNoninteractable

# %% Core page class
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
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        # Variables in this reactor core page instance
        # Colors of different kinds of elements TODO: make this editable w toolbar
        self.element_colors = {"Base": "light gray", "Instrument": "white smoke",
                               "Imaging Chamber": "spring green", "Sample Chamber": "bisque",
                               "Fuel Storage": "turquoise", "Fuel Bundle": "powder blue",
                               "Fuel Rod": "sky blue", "Control Rod": "pink", "Sample": "light goldenrod",
                               "Control Button": "lemon chiffon", "Element Button":"floral white", "Background": "white"}
        # Dictionaries that basically hold all the configuration information
        # Element_name: grid coords (topleft [0-9][A-Z], bottomright [0-9][A-Z])
        self.core_element_coordinates = {}
        self.controls_element_coordinates = {}
        # Element_name: element_type
        self.core_element_types = {}
        self.controls_element_types = {}
        # # Fuel element_name: fuel element_contains
        # self.fuel_bundles = {}
        # # Sample element_name: sample element_contains
        # self.samples = {}
        # # Buttons
        # self.buttons = {}
        self.elements = {}
        
        # FIXME: Turn this into board_state.Loading()
        self.state = board_state.Loading()

        # Set up page properties

        # self.grid_rowconfigure(0, weight=1, minsize=controller.cell_size)
        # self.grid_columnconfigure(0, weight=1, minsize=controller.cell_size)

        # TODO: something to set up the actual core's cooordinates

        self.core_canvas = tk.Canvas(self, 
                                     height=self.controller.height,
                                     width=self.controller.width * self.controller.NUM_CORE_LENGTH_BLOCKS / self.controller.NUM_LENGTH_BLOCKS,
                                     bg=self.element_colors["Background"]
                                     )

        self.controls_canvas = tk.Canvas(self,
                                         height=self.controller.height,
                                         width=self.controller.width * self.controller.NUM_CONTROLS_LENGTH_BLOCKS / self.controller.NUM_LENGTH_BLOCKS,
                                         bg=self.element_colors["Background"]
                                         )

        self.core_canvas.grid(row=0, column=0)
        self.controls_canvas.grid(row=0, column=1)

        # Load core if config exists
        if not self.load_configuration():
            # TODO: request for new .csv file from user
            self.controller.destroy()
            self.controller.popup_message("configuration csv file not found!")
        else:
            self.update_core()
    
    def __repr__(self):
        return "{self.__class__.__name__}(parent={self.parent}, controller={self.controller})".format(self=self)

    def load_configuration(self, filename="./configuration.csv"):
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
                    temp_name = row["Element Name"]
                    temp_type = row["Element Type"]
                    temp_canvas = row["Canvas"]
                    temp_topleft = row["Top Left Coordinate"]
                    temp_bottomright = row["Bottom Right Coordinate"]
                    temp_contains = row["Contains"]

                    if (temp_type in set(self.element_colors.keys())):
                        # Update variables (dictionaries)
                        if (temp_canvas == "Core"):
                            self.core_element_types[temp_name] = temp_type
                            self.core_element_coordinates[temp_name] = (temp_topleft, temp_bottomright)
                        elif (temp_canvas == "Controls"):
                            self.controls_element_types[temp_name] = temp_type
                            self.controls_element_coordinates[temp_name] = (temp_topleft, temp_bottomright)

                        # if (temp_type == "Fuel Bundle"):
                        #     self.fuel_bundles[temp_name] = temp_contains
                        # elif (temp_type == "Sample"):
                        #     self.samples[temp_name] = temp_contains

                        # TODO: move drawing outside of this function, put it in __init__ with a "update page" or smth
                        # Draw element
                        if not self.draw_element(temp_name, temp_type, temp_canvas, temp_topleft, temp_bottomright, temp_contains):
                            raise ValueError("Element " + temp_name + " could not be drawn")

                    else:
                        raise ValueError("Invalid element type: " + temp_type)

            self.change_state(board_state.Ready)
            return True

        except FileNotFoundError as e:
            print(e)
            return False
        except csv.Error as e:
            print(e)
            return False
        except ValueError as e:
            print(e)
            return False

    def update_core(self):
        """
        Updates the core page elements based on its state

        Parameters:
            None

        Returns:
            None
        """
        if (self.state.equals(board_state.Ready)):
            # Enable control buttons
            self.control_buttons_enable()
            # Hide all core buttons
            pass
        elif (self.state.equals(board_state.MoveFuelSelectFuel)):
            # Pop-up
            self.controller.popup_message("Choose a fuel bundle to move")
            # Disable control buttons
            self.control_buttons_disable()
            # Show fuel bundle select buttons
            self.fuel_bundle_buttons_show()
            # Show fuel storage select buttons
            pass
        elif (self.state == board_state.MoveFuelSelectPlace):
            # Pop-up
            # Hide fuel bundle/fuel storage buttons
            pass
        print(self.state)

    def change_state_string(self, state_string):
        """
        Changes the state of the CorePage instance and updates core
        
        Parameters:
            state (string): A string representing the state the core will change to.
                If it is not a valid state string, raises a ValueError
        
        Returns:
            None
        """
        if (state_string == "Ready"):
            self.state.switch(board_state.Ready)
        if (state_string == "Move Fuel"):
            self.state.switch(board_state.MoveFuelSelectFuel)
        elif (state_string == "Add Fuel"):
            self.state.switch(board_state.AddFuelSelectPlace)
        elif (state_string == "Remove Fuel"):
            self.state.switch(board_state.RemoveFuelSelectFuel)
        elif (state_string == "Add Sample"):
            self.state.switch(board_state.AddSampleSelectPlace)
        elif (state_string == "Remove Sample"):
            self.state.switch(board_state.RemoveSampleSelectSample)
        else: 
            raise ValueError("Invalid state string")

        self.update_core()
    
    def change_state(self, state):
        """
        Changes the state of the CorePage instance

        Parameters:
            state (Class): A subclass of BoardState as specified in board_state.py;
                the state to change to. If it is not a valid state or the state
                change is invalid, raises a ValueError
        
        Returns:
            None
        """
        self.state.switch(state)
        self.update_core()

    def draw_element(self, name, element_type, canvas, topleft_coordinate, bottomright_coordinate, contains=None):
        """
        Draws an element specified by method parameters

        Parameters:
            element_type (String): The type of element. Must be a valid type
            name (String): Name of the element, usually used to label it
            topleft_px (tuple): (x,y) tuple of the element's top left px position
                bottomright_px (tuple): (x,y) tuple of the element's bottom right px position
                contains (String): Stuff contained in this element. See configuration.csv for details

        Returns:
            True (boolean) if the element was successfully drawn, False otherwise
        """
        if element_type in set(self.element_colors.keys()):
            # FIXME: Do something to prevent duplicate names from happened
            # Convert coordinates into pixels
            (topleft_px, bottomright_px) = self.get_pxlocation(topleft_coordinate, bottomright_coordinate)

            # If it's a control button element, draw in controls_canvas
            if (element_type == "Control Button"):
                self.elements[name] = ElementControlButton(self, self.controls_canvas, name, element_type, topleft_px, bottomright_px, contains)
            # If it's a fuel bundle (requires contains variable)
            elif (element_type == "Fuel Bundle") and contains:
                self.elements[name] = ElementFuelBundle(self, self.core_canvas, name, element_type, topleft_px, bottomright_px, contains)
            # If it's a fuel storage element
            elif (element_type == "Fuel Storage"):
                self.elements[name] = ElementFuelStorage(self, self.core_canvas, name, element_type, topleft_px, bottomright_px, contains)
            # If it's a sample
            elif (element_type == "Sample"):
                self.elements[name] = ElementSample(self, self.core_canvas, name, element_type, topleft_px, bottomright_px, contains)
            # If it's a sample chamber
            elif (element_type == "Sample Chamber"):
                self.elements[name] = ElementSampleChamber(self, self.core_canvas, name, element_type, topleft_px, bottomright_px, contains)
            # If it's any other kind of element (Base, Instrument), it doesn't interact with anything (for now at least)
            else:
                self.elements[name] = ElementNoninteractable(self, self.core_canvas, name, element_type, topleft_px, bottomright_px, contains)

            self.elements[name].draw()

            return True

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

    ############ Command methods
    def control_buttons_disable(self):
        print("TEST CONTROL")
        for element in self.elements.values():
            if element.get_type() == "Control Button":
                element.disable()

    def control_buttons_enable(self):
        for element in self.elements.values():
            if element.get_type() == "Control Button":
                element.enable()
    
    def fuel_bundle_buttons_show(self):
        print("TEST FUEL")
        for element in self.elements.values():
            if element.get_type() == "Fuel Bundle":
                element.button_show()