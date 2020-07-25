# -*- coding: utf-8 -*-
"""
Abstract class for elements in the status board

Conducted under the Unversity of Maryland
Created on Fri Jul 24 17:12:36 2020
@author: Telon J. Yan
"""
# %% Imoprts
from abc import ABC, abstractmethod
import tkinter as tk

class AbstractElement(tk.Canvas, ABC):

    def __init__(self, page, canvas, name, element_type, topleft_coordinate, bottomright_coordinate, contains=None):
        (topleft_px, bottomright_px) = page.get_pxlocation(topleft_coordinate, bottomright_coordinate)
        
        super().__init__(canvas, width=bottomright_px[0]-topleft_px[0], height=bottomright_px[1]-topleft_px[1], bg = page.ELEMENT_COLORS["Background"])
        
        self.name = name
        self.element_type = element_type
        self.topleft_coordinate = topleft_coordinate
        self.bottomright_coordinate = bottomright_coordinate
        self.contains = contains
        self.interactable = False

    def get_name(self):
        return self.name
    
    def get_position(self):
        return (self.topleft_coordinate, self.bottomright_coordinate)

    def set_position(self, coordinates):
        self.topleft_coordinate = coordinates[0]
        self.bottomright_coordinate = coordinates[1]

    def get_type(self):
        return self.element_type

    def is_interactable(self):
        return self.interactable

    def set_interactable(self, interactable):
        self.interactable = interactable

    @abstractmethod
    def hide(self):
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def draw(self):
        pass