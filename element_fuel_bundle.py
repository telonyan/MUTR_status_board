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

    def __init__(self, page, canvas, name, element_type, topleft_px, bottomright_px, contains=None):
        super().__init__(page, canvas, name, element_type, topleft_px, bottomright_px, contains)
        self.set_interactable(True)
        self.rods = self.contains.split(",")

    def draw(self):
        
        # Draw background
        self.create_rectangle(0,0,self.width,self.height,fill=self.page.element_colors[self.element_type])
        
        # Draw "rods"
        # Top left rod
        self.create_oval(0, 0, self.width/2, self.height/2, fill=self.page.element_colors["Fuel Rod" if self.rods[0].isnumeric() else "Control Rod"])
        self.create_text(self.width/4, self.height/4, text=self.rods[0], font=self.page.controller.SMALL_FONT)
        # Top right rod
        self.create_oval(self.width/2, 0, self.width, self.height/2, fill=self.page.element_colors["Fuel Rod" if self.rods[1].isnumeric() else "Control Rod"])
        self.create_text(self.width*3/4, self.height/4, text=self.rods[1], font=self.page.controller.SMALL_FONT)
        # Bottom left rod
        self.create_oval(0, self.height/2, self.width/2, self.height, fill=self.page.element_colors["Fuel Rod" if self.rods[2].isnumeric() else "Control Rod"])
        self.create_text(self.width/4, self.height*3/4, text=self.rods[2], font=self.page.controller.SMALL_FONT)
        # Bottom right rod
        self.create_oval(self.width/2, self.height/2, self.width, self.height, fill=self.page.element_colors["Fuel Rod" if self.rods[3].isnumeric() else "Control Rod"])
        self.create_text(self.width*3/4, self.height*3/4, text=self.rods[3], font=self.page.controller.SMALL_FONT)

        # TODO: Add buttons and hide them
        self.select_button = tk.Button(self, 
                                       bg=self.page.element_colors["Element Button"],
                                       text="Select",
                                       font=self.page.controller.SMALL_FONT,
                                       )
        # Width and height are only really important here, not in the Button instantiation
        self.select_button.place(x=self.width/2-self.page.controller.cell_size/2, 
                                 y=self.height/2-self.page.controller.cell_size/4, 
                                 width=self.page.controller.cell_size, 
                                 height=self.page.controller.cell_size/2
                                 )
        self.select_button.place_forget()
        

    # TODO: Add functions to deal with the buttons
    def button_show(self):
        self.select_button.place()
    
    def button_hide(self):
        self.select_button.place_forget()