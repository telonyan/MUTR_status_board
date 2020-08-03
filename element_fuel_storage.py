# -*- coding: utf-8 -*-
"""
Class for fuel storage elements in the status board, a child of AbstractElement

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""
# %% Imports
from element_abstract import ElementAbstract
import tkinter as tk

# %% Control Button elements class
class ElementFuelStorage(ElementAbstract):

    def __init__(self, page, canvas, name, element_type, topleft_px, bottomright_px, contains=None):
        super().__init__(page, canvas, name, element_type, topleft_px, bottomright_px, contains)
        self.set_interactable(True)

    def draw(self):
        self.create_rectangle(0,0,self.width,self.height,fill=self.page.element_colors[self.element_type])
        self.create_text(self.width/2, 
                         self.height/2, 
                         text=self.name, 
                         font=self.page.controller.MEDIUM_FONT,
                         width=self.width
                         )
        # TODO: Add buttons and hide them
    
    # TODO: Add functions to deal with the buttons