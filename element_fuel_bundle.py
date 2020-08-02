# -*- coding: utf-8 -*-
"""
Class for fuel bundle elements in the status board, a child of AbstractElement

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""
# %% Imports
from element_abstract import ElementAbstract
import tkinter as tk

# %% Control Button elements class
class ElementFuelBundle(ElementAbstract):

    def draw(self):
        self.create_rectangle(0,0,self.width,self.height,fill=self.page.element_colors[self.element_type])
        rods = self.contains.split(",")
        # Top left rod
        self.create_oval(0, 0, self.width/2, self.height/2, fill=self.page.element_colors["Fuel Rod" if rods[0].isnumeric() else "Control Rod"])
        self.create_text(self.width/4, self.height/4, text=rods[0], font=self.page.controller.SMALL_FONT)
        # Top right rod
        self.create_oval(self.width/2, 0, self.width, self.height/2, fill=self.page.element_colors["Fuel Rod" if rods[1].isnumeric() else "Control Rod"])
        self.create_text(self.width*3/4, self.height/4, text=rods[1], font=self.page.controller.SMALL_FONT)
        # Bottom left rod
        self.create_oval(0, self.height/2, self.width/2, self.height, fill=self.page.element_colors["Fuel Rod" if rods[2].isnumeric() else "Control Rod"])
        self.create_text(self.width/4, self.height*3/4, text=rods[2], font=self.page.controller.SMALL_FONT)
        # Bottom right rod
        self.create_oval(self.width/2, self.height/2, self.width, self.height, fill=self.page.element_colors["Fuel Rod" if rods[3].isnumeric() else "Control Rod"])
        self.create_text(self.width*3/4, self.height*3/4, text=rods[3], font=self.page.controller.SMALL_FONT)