# -*- coding: utf-8 -*-
"""
Core States

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""

class CoreState(object):

    name = "state"
    allowed = []

    def switch(self, state):
        """ Switch to new state """
        if state.name in self.allowed:
            self.__class__ = state
        else:
            raise ValueError
    
    def __str__(self):
        return self.name

class Ready(CoreState):
    name = "ready"
    allowed = ["move_fuel_select_fuel", 
               "add_fuel_select_place", 
               "remove_fuel_select_fuel", 
               "add_sample_select_place", 
               "remove_sample_select_sample"
               ]

class MoveFuelSelectFuel(CoreState):
    name = "move_fuel_select_fuel"
    allowed = ["move_fuel_select_place"]

class MoveFuelSelectPlace(CoreState):
    name = "move_fuel_select_place"
    allowed = ["ready"]

class AddFuelSelectPlace(CoreState):
    name = "add_fuel_select_place"
    allowed = ["add_fuel_specify_fuel"]

class AddFuelSpecifyFuel(CoreState):
    name = "add_fuel_specify_fuel"
    allowed = ["ready"]

class RemoveFuelSelectFuel(CoreState):
    name = "remove_fuel_select_fuel"
    allowed = ["ready"]

class AddSampleSelectPlace(CoreState):
    name = "add_sample_select_place"
    allowed = ["add_sample_specify_sample"]

class AddSampleSpecifySample(CoreState):
    name = "add_sample_specify_sample"
    allowed = ["ready"]

class RemoveSampleSelectSample(CoreState):
    name = "remove_sample_select_sample"
    allowed = ["ready"]