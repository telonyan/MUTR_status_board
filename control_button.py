# -*- coding: utf-8 -*-
"""
Abstract class for elements in the status board

Conducted under the Unversity of Maryland
Created on Wed Jul 28 21:43:44 2020
@author: Telon J. Yan
"""
# %% Imports
from abstract_element import AbstractElement
import tkinter as tk

# %% Control Button elements class
class ControlButton(AbstractElement):
    # TODO: DOCUMENTATION

    def __init__(self, page, canvas, name, element_type, topleft_px, bottomright_px, contains=None):
        super().__init__(page, canvas, name, element_type, topleft_px, bottomright_px, contains)
        self.set_interactable(True)

    def draw(self):
        # FIXME: needs command
        self.button = tk.Button(self.canvas, 
                                bg=self.page.element_colors["Control Button"],
                                text=self.name,
                                font=self.page.controller.MEDIUM_FONT,
                                wrap=self.width,
                                width=self.width,
                                height=self.height
                                )
        self.button.place(x=self.topleft_px[0], y=self.topleft_px[1], height=self.height, width=self.width)
