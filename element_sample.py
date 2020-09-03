# -*- coding: utf-8 -*-
"""
Class for noninteractable elements in the status board, a child of AbstractElement

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""
# %% Imports
from element_abstract import ElementAbstract
import tkinter as tk
import warnings

# %% Control Button elements class
class ElementSample(ElementAbstract):

    def draw(self):
        warnings.warn(DeprecationWarning)

    # TODO: ????