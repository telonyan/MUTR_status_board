# -*- coding: utf-8 -*-
"""
Board State class and State Classes

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""

class BoardState(object):

    name = "state"
    allowed = []

    def switch(self, state):
        """ Switch to new state """
        if state.name in self.allowed:
            self.__class__ = state
        else:
            raise ValueError("Invalid state switch from current state: " + str(self) + " to target state: " + state.name)
    
    def equals(self, state):
        if self.name == state.name:
            return True
        return False

    def __str__(self):
        return self.name

class Loading(BoardState):
    name = "loading"
    allowed = ["ready"]

class Ready(BoardState):
    name = "ready"
    allowed = ["move_fuel_select_fuel", 
               "add_fuel_select_place", 
               "remove_fuel_select_fuel", 
               "add_sample_select_place", 
               "remove_sample_select_sample"
               ]

class MoveFuelSelectFuel(BoardState):
    name = "move_fuel_select_fuel"
    allowed = ["move_fuel_select_place"]

class MoveFuelSelectPlace(BoardState):
    name = "move_fuel_select_place"
    allowed = ["ready"]

class AddFuelSelectPlace(BoardState):
    name = "add_fuel_select_place"
    allowed = ["add_fuel_specify_fuel"]

class AddFuelSpecifyFuel(BoardState):
    name = "add_fuel_specify_fuel"
    allowed = ["ready"]

class RemoveFuelSelectFuel(BoardState):
    name = "remove_fuel_select_fuel"
    allowed = ["ready"]

class AddSampleSelectPlace(BoardState):
    name = "add_sample_select_place"
    allowed = ["add_sample_specify_sample"]

class AddSampleSpecifySample(BoardState):
    name = "add_sample_specify_sample"
    allowed = ["ready"]

class RemoveSampleSelectSample(BoardState):
    name = "remove_sample_select_sample"
    allowed = ["ready"]