# -*- coding: utf-8 -*-
"""
Temporary test page of the MUTR Status board

Conducted under the Unversity of Maryland Radiation Facilities

@author: Telon J. Yan
"""
# %% Imports
import tkinter as tk

# %% Other page class
class TestPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_label = tk.Label(self, text="This is page 1",
                               font=controller.LARGE_FONT)
        title_label.pack(side="top", fill="x", pady=10)

        button0 = tk.Button(self, text="Go to the core page", font=controller.SMALL_FONT,
                            command=lambda: controller.show_frame("CorePage"))
        button0.pack()
