# -*- coding: utf-8 -*-
"""
Temporary test page of the MUTR Status board

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""
# %% Imports
import tkinter as tk

# %% Other page class
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        # TODO: DOCUMENTATION
        # TODO: select config file

        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_label = tk.Label(self, text="Choose a configuration csv file",
                               font=controller.LARGE_FONT)
        title_label.pack(side="top", fill="x", pady=10)

        button0 = tk.Button(self, text="Select", font=controller.SMALL_FONT,
                            command=lambda: controller.show_frame("CorePage"))
        button0.pack()
