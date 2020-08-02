# -*- coding: utf-8 -*-
"""
An interactive status board for the Maryland University Training Reactor (MUTR)

Conducted under the Unversity of Maryland
Created on Tue Jun 23 10:57:39 2020
@author: Telon J. Yan
"""
from status_board import StatusBoard

if __name__ == "__main__":
    master = StatusBoard()
    master.mainloop()