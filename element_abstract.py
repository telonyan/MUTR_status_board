# -*- coding: utf-8 -*-
"""
Abstract class for elements in the status board

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""
# %% Imports
from abc import ABC, abstractmethod
import tkinter as tk

# %% Abstract Element of reactor core class
class ElementAbstract(tk.Canvas, ABC):
    # TODO: DOCUMENTATION

    def __init__(self, page, canvas, name, element_type, topleft_px, bottomright_px, contains=None):
        # TODO: DOCUMENTATION
        super().__init__(canvas, 
                         width=bottomright_px[0]-topleft_px[0], 
                         height=bottomright_px[1]-topleft_px[1], 
                         bg=page.element_colors["Background"], 
                         highlightthickness=0
                         )
        # Assign instance variables = parameters
        self.page = page
        self.canvas = canvas
        self.name = name
        self.element_type = element_type
        self.topleft_px = topleft_px
        self.bottomright_px = bottomright_px
        self.contains = contains
        # Calculate variables based on parameters
        self.width = self.bottomright_px[0]-self.topleft_px[0]
        self.height = self.bottomright_px[1]-self.topleft_px[1]
        self.center_px = ((self.topleft_px[0]+self.bottomright_px[0])/2, (self.topleft_px[1]+self.bottomright_px[1])/2)
        self.interactable = False

        self.place(x=self.topleft_px[0], y=self.topleft_px[1], height=self.height, width=self.width)

    def get_name(self):
        return self.name
    
    def get_position(self):
        return (self.topleft_px, self.bottomright_px)

    def set_position(self, coordinates_px):
        self.topleft_px = coordinates_px[0]
        self.bottomright_px = coordinates_px[1]

    def get_type(self):
        return self.element_type

    def is_interactable(self):
        # TODO: DOCUMENTATION
        return self.interactable

    def set_interactable(self, interactable):
        # TODO: DOCUMENTATION
        if interactable == True or interactable == False:
            self.interactable = interactable
        else:
            raise ValueError

    def hide(self):
        # TODO: DOCUMENTATION
        self.place_forget()

    def show(self):
        # TODO: DOCUMENTATION
        self.place(x=self.topleft_px[0], y=self.topleft_px[1], height=self.height, width=self.width)

    @abstractmethod
    def draw(self):
        # TODO: DOCUMENTATION
        pass