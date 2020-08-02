# -*- coding: utf-8 -*-
"""
Class for noninteractable elements in the status board, a child of AbstractElement

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""
# %% Imports
from element_abstract import ElementAbstract
import tkinter as tk

# %% Control Button elements class
class ElementNoninteractable(ElementAbstract):

    def draw(self):
        self.create_rectangle(0,0,self.width,self.height,fill=self.page.element_colors[self.element_type])
        self.create_text(self.width/2, 
                         self.height/2, 
                         text=self.name, 
                         font=self.page.controller.MEDIUM_FONT,
                         width=self.width
                         )