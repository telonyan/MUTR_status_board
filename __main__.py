# -*- coding: utf-8 -*-
"""
An interactive status board for the Maryland University Training Reactor (MUTR)

Conducted under the Unversity of Maryland
Created on Tue Jun 23 10:57:39 2020
@author: Telon J. Yan
"""
from status_board import StatusBoard

master = StatusBoard()
master.geometry("1280x720")
master.mainloop()