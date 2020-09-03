# -*- coding: utf-8 -*-
"""
Class for control button elements in the status board, a child of AbstractElement

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""
# %% Imports
from element_abstract import ElementAbstract
import tkinter as tk

# %% Control Button elements class
class ElementControlButton(ElementAbstract):
    # TODO: DOCUMENTATION

    def __init__(self, page, canvas, name, element_type, topleft_px, bottomright_px, contains=None):
        super().__init__(page, canvas, name, element_type, topleft_px, bottomright_px, contains)
        # FIXME: force this to take a boolean or smth
        self.set_interactable(True)

    def draw(self):
        # FIXME: needs command
        self.button = tk.Button(self, 
                                bg=self.page.element_colors[self.element_type],
                                text=self.name,
                                font=self.page.controller.MEDIUM_FONT,
                                wrap=self.width,
                                width=self.width,
                                height=self.height,
                                command=lambda: self.page.change_state_string(self.name)
                                )
        # Width and height are only really important here, not in the Button instantiation
        self.button.place(x=0, y=0, width=self.width, height=self.height)

    def disable(self):
        self.button["state"] = tk.DISABLED
    
    def enable(self):
        self.button["state"] = tk.NORMAL